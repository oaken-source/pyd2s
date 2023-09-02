
'''
this module provides classes to manage item data of a d2s save
'''

import os
import struct

from pyd2s.item import Item, ExtendedItem
from pyd2s.character import Character, CharacterClass


class ItemData:
    '''
    save data related to item
    '''
    def __init__(self, buffer, offset):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer
        self._offset = offset

        self._pdata = []
        self._cdata = []
        self._mdata = []
        self._gdata = []

        if self._header != 'JM':
            raise ValueError('invalid save: mismatched player item data section header')

        # we can stop looking for item data on a sparse input file
        if self._buffer.sparse:
            return

        ptr = self._offset + 2

        # player items
        pcount = struct.unpack_from('<H', self._buffer, ptr)[0]
        ptr += 2
        for _ in range(pcount):
            item = Item.from_data(self._buffer, ptr)
            ptr += item.length
            self._pdata.append(item)

        # corpse items
        ccount = 0
        if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
            raise ValueError('invalid save: mismatched corpse item data section header')
        ptr += 2
        ccount = struct.unpack_from('<H', self._buffer, ptr)[0]
        ptr += 2
        if ccount == 1:
            ptr += 12
            if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
                raise ValueError('invalid save: mismatched corpse item data section header')
            ptr += 2
            ccount = struct.unpack_from('<H', self._buffer, ptr)[0]
            ptr += 2
            for _ in range(ccount):
                item = Item.from_data(self._buffer, ptr)
                ptr += item.length
                self._cdata.append(item)

        # mercenary items
        if Character(self._buffer).is_expansion:
            if self._buffer[ptr:ptr+2].decode('ascii') != 'jf':
                raise ValueError('invalid save: mismatched mercenary item data section header')
            ptr += 2
            if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
                raise ValueError('invalid save: mismatched corpse item data section header')
            ptr += 2
            mcount = struct.unpack_from('<H', self._buffer, ptr)[0]
            ptr += 2
            for _ in range(mcount):
                item = Item.from_data(self._buffer, ptr)
                ptr += item.length
                self._mdata.append(item)
            if self._buffer[ptr:ptr+2].decode('ascii') != 'kf':
                raise ValueError('invalid save: mismatched mercenary item data section header')
            ptr += 2

        # golem items
        if Character(self._buffer).character_class == CharacterClass.NECROMANCER:
            gcount = self._buffer[ptr]
            ptr += 1
            if gcount == 1:
                item = Item.from_data(self._buffer, ptr)
                ptr += item.length
                self._gdata.append(item)

        if ptr != len(self._buffer):
            raise ValueError('invalid save: trailing data')

        # all items were verified, use them to generate test data
        for item in self._pdata + self._cdata + self._mdata + self._gdata:
            data = item.rawdata

            key = item.name
            if isinstance(item, ExtendedItem):
                key += f' - {item.uid:#010x}'

            path = f'tests/itemdata/{key}.data'
            if os.path.exists(path):
                continue

            print(f'writing testdata for item {key}')
            staging_path = f'tests/itemdata/new/{key}.data'
            with open(staging_path, 'wb') as itemfile:
                itemfile.write(data)

            staging_path = f'tests/itemdata/new/{key}.desc'
            with open(staging_path, 'w', encoding='ascii') as descfile:
                descfile.write(str(item))

    @property
    def _header(self):
        '''
        produce the header of the items section - should be 'JM'
        '''
        if self._buffer.sparse:
            return 'JM'
        return self._buffer[self._offset:self._offset + 2].decode('ascii')

    @property
    def pcount(self):
        '''
        player item count
        '''
        return len(self._pdata)

    def getpdata(self, index):
        '''
        Get player item data
        '''
        return self._pdata[index]

    @property
    def ccount(self):
        '''
        corpse item count
        '''
        return len(self._cdata)

    def getcdata(self, index):
        '''
        Get corpse item data
        '''
        return self._cdata[index]

    @property
    def mcount(self):
        '''
        mercenary item count
        '''
        return len(self._mdata)

    def getmdata(self, index):
        '''
        Get mercenary item data
        '''
        return self._mdata[index]

    @property
    def gcount(self):
        '''
        iron golem item count
        '''
        return len(self._gdata)

    def getgdata(self, index):
        '''
        Get iron golem item data
        '''
        return self._gdata[index]
