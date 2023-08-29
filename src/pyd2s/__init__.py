
'''
This module provides classes to manage D2 save games.
'''

import struct

from pyd2s.savebuffer import SaveBuffer
from pyd2s.character import Character
from pyd2s.mercenary import Mercenary
from pyd2s.itemdata import ItemData
from pyd2s.questdata import QuestData
from pyd2s.waypointdata import WaypointData


class D2SaveFile:
    '''
    a .d2s file containing diablo 2 save game data
    '''

    def __init__(self, path):
        '''
        constructor - initialize buffer and do sanity checks
        '''
        self._buffer = SaveBuffer(path)

        if self.magic != 0xaa55aa55:
            raise ValueError('invalid save: mismatched magic number')
        if self.version != 0x60:
            raise ValueError('invalid save: pre 1.10 saves are not supported')
        if len(self._buffer) <= 335:
            raise ValueError('invalid save: truncated data?')

        self.character = Character(self._buffer)
        self.mercenary = Mercenary(self._buffer)
        self.questdata = QuestData(self._buffer)
        self.waypointdata = WaypointData(self._buffer)
        self.itemdata = ItemData(self._buffer)

    @property
    def magic(self):
        '''
        get the magic number of d2s files - should be 0xaa55aa55
        '''
        return struct.unpack_from('<L', self._buffer)[0]

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
        tmp = D2SaveFile(self._buffer.path)
        if tmp.timestamp > self.timestamp:
            raise ValueError('flush failed: refusing to overwrite newer version')
        self._buffer.flush()
