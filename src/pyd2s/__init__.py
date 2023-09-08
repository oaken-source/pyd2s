'''
This module provides classes to manage D2 save games.
'''

import struct
import logging
from enum import Enum

from pyd2s.savebuffer import SaveBuffer
from pyd2s.character import Character
from pyd2s.mercenary import Mercenary
from pyd2s.itemdata import ItemData
from pyd2s.item import Item
from pyd2s.questdata import QuestData
from pyd2s.waypointdata import WaypointData
from pyd2s.plugydata import PlugyStashPage


class SaveFile:
    '''
    a file containing diablo 2 save data.

    currently supported files are:
        - .d2s files containing full character saves
        - .d2i files containing data of a single item
        - .sss files containing shared PlugY stash data
        - .d2x files containing personal PlugY stash data
    '''

    class Type(Enum):
        '''
        the different types of save files
        '''
        D2S = 0  # full save
        D2I = 1  # item data
        SSS = 2  # PlugY shared stash
        D2X = 3  # PlugY personal stash

    @classmethod
    def open(cls, path):
        '''
        open a file by path and parse the data
        '''
        buffer = SaveBuffer(path)
        return cls.from_buffer(buffer)

    @classmethod
    def from_buffer(cls, buffer):
        '''
        open a file from a given savebuffer
        '''
        if not isinstance(buffer, SaveBuffer):
            raise TypeError('usage: buffer must be pyd2s.SaveBuffer instance')

        if struct.unpack_from('<L', buffer)[0] == 0xaa55aa55:
            return D2SaveFile(buffer)
        if buffer[:2].decode('ascii') == 'JM':
            return D2ItemFile(buffer)
        if buffer[:4].decode('ascii') == 'SSS\0':
            return PlugySharedStash(buffer)
        if buffer[:4].decode('ascii') == 'CSTM':
            return PlugyPersonalStash(buffer)

        raise ValueError('invalid save: unrecognized file header')


class D2SaveFile:
    '''
    a .d2s file containing diablo 2 save game data
    '''
    def __init__(self, buffer):
        '''
        constructor - initialize buffer and do sanity checks
        '''
        logging.debug('D2SaveFile:__init__')
        self._buffer = buffer

        if self.magic != 0xaa55aa55:
            raise ValueError('invalid save: mismatched magic number')
        if self.version != 0x60:
            raise ValueError('invalid save: pre 1.10 and post 1.14 saves are not supported')
        if len(self._buffer) < 335:
            raise ValueError('invalid save: truncated data')

        if self._buffer.sparse:
            logging.warning('sparse save: has never been saved in-game.')

        self.character = Character(self._buffer)
        self.mercenary = Mercenary(self._buffer)
        self.questdata = QuestData(self._buffer)
        self.waypointdata = WaypointData(self._buffer)
        self.itemdata = ItemData(self, self._buffer, 765 + self.character.stats.length + 32)

    @property
    def type(self):
        '''
        indicate the type of save file this is
        '''
        return SaveFile.Type.D2S

    @property
    def magic(self):
        '''
        get the magic number of d2s files - should be 0xaa55aa55
        '''
        return struct.unpack_from('<L', self._buffer, 0)[0]

    @property
    def version(self):
        '''
        get the version of the file - supported values are 0x60 for >=1.10
        '''
        return struct.unpack_from('<L', self._buffer, 0x04)[0]

    @property
    def timestamp(self):
        '''
        get the last save timestamp
        '''
        return struct.unpack_from('<L', self._buffer, 0x30)[0]

    def flush(self):
        '''
        flush the save data back to file, if not newer on disk
        '''
        tmp = SaveFile.open(self._buffer.path)
        if tmp.timestamp > self.timestamp:
            raise ValueError('flush failed: refusing to overwrite newer version')
        self._buffer.flush()


class D2ItemFile:
    '''
    a .d2i file containing data for exactly one item
    '''
    def __init__(self, buffer):
        '''
        constructor - initialize buffer and do sanity checks
        '''
        self._buffer = buffer

        if self.header != 'JM':
            raise ValueError('invalid save: invalid item header')

        self._item = Item.from_data(buffer, 0)

        if len(buffer) != self._item.length:
            raise ValueError('invalid save: trailing data')

    @property
    def version(self):
        '''
        .d2i files are always version 0x60
        '''
        return 0x60

    @property
    def type(self):
        '''
        indicate the type of save file this is
        '''
        return SaveFile.Type.D2I

    @property
    def header(self):
        '''
        produce the header of the item file
        '''
        return self._buffer[:2].decode('ascii')

    @property
    def item(self):
        '''
        produce the item of the item file
        '''
        return self._item


class PlugySharedStash:
    '''
    an .xxx file containing shared stash data
    '''
    def __init__(self, buffer):
        '''
        constructor - initialize buffer and do sanity checks
        '''
        self._buffer = buffer

        if self.header != 'SSS\0':
            raise ValueError('invalid save: mismatched file header')

        ptr = 6

        self._stored_gold = 0
        if self.version == 2:
            self._stored_gold = struct.unpack_from('<L', self._buffer, ptr)[0]
            ptr += 4

        num_pages = struct.unpack_from('<L', self._buffer, ptr)[0]
        ptr += 4

        self._pages = []
        for _ in range(num_pages):
            page = PlugyStashPage(self._buffer, ptr)
            ptr += page.length
            self._pages.append(page)

    @property
    def type(self):
        '''
        indicate the type of save file this is
        '''
        return SaveFile.Type.SSS

    @property
    def header(self):
        '''
        the header of the stash file
        '''
        return self._buffer[:4].decode('ascii')

    @property
    def version(self):
        '''
        the version of the stash file
        '''
        return int(self._buffer[4:6].decode('ascii'))

    @property
    def stored_gold(self):
        '''
        the amount of gold stored in the stash, only if version == 2
        '''
        return self._stored_gold

    @property
    def pages(self):
        '''
        the pages in the stash
        '''
        return self._pages


class PlugyPersonalStash:
    '''
    a .d2x file containing personal stash data
    '''
    def __init__(self, buffer):
        '''
        constructor - initialize buffer and do sanity checks
        '''
        self._buffer = buffer

        if self.header != 'CSTM':
            raise ValueError('invalid save: mismatched file header')
        if self.version != 1:
            raise ValueError('invalid save: unrecognized version header')

        ptr = 10

        num_pages = struct.unpack_from('<L', self._buffer, ptr)[0]
        ptr += 4

        self._pages = []
        for _ in range(num_pages):
            page = PlugyStashPage(self._buffer, ptr)
            ptr += page.length
            self._pages.append(page)

    @property
    def type(self):
        '''
        indicate the type of save file this is
        '''
        return SaveFile.Type.D2X

    @property
    def header(self):
        '''
        the header of the stash file
        '''
        return self._buffer[:4].decode('ascii')

    @property
    def version(self):
        '''
        the version of the stash file
        '''
        return int(self._buffer[4:6].decode('ascii'))

    @property
    def pages(self):
        '''
        the pages in the stash
        '''
        return self._pages
