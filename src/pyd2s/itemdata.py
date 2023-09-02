
'''
this module provides classes to manage item data of a d2s save
'''

import struct

from pyd2s.item import Item
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

        # items on player / belt / cursor / in stash
        self._pdata = []
        # items on player corpse, if any
        self._cdata = []
        # items on mercenary, if any
        self._mdata = []
        # iron golem
        self._gdata = []

        if self._header != 'JM':
            raise ValueError('invalid save: mismatched item data section header')

        # we can stop looking for item data on a sparse input file
        if self._buffer.sparse:
            return

        ptr = self._offset + 2

        ptr = self._read_pdata(ptr)
        ptr = self._read_cdata(ptr)
        ptr = self._read_mdata(ptr)
        ptr = self._read_gdata(ptr)

        if ptr != len(self._buffer):
            raise ValueError('invalid save: trailing data')

    def _read_pdata(self, ptr):
        '''
        parse player item data from the save buffer
        '''
        pcount = struct.unpack_from('<H', self._buffer, ptr)[0]
        ptr += 2

        for _ in range(pcount):
            item = Item.from_data(self._buffer, ptr)
            ptr += item.length
            self._pdata.append(item)

        return ptr

    def _read_cdata(self, ptr):
        '''
        parse player corpse item data from the save buffer
        '''
        if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
            raise ValueError('invalid save: mismatched corpse item data section header')
        ptr += 2

        ccount = struct.unpack_from('<H', self._buffer, ptr)[0]
        ptr += 2

        if ccount == 0:
            return ptr

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

        return ptr

    def _read_mdata(self, ptr):
        '''
        parse mercenary item data from the save buffer
        '''
        if not Character(self._buffer).is_expansion:
            return ptr

        if self._buffer[ptr:ptr+2].decode('ascii') != 'jf':
            raise ValueError('invalid save: mismatched mercenary item data section header')
        ptr += 2

        if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
            raise ValueError('invalid save: mismatched mercenary item data section header')
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

        return ptr

    def _read_gdata(self, ptr):
        '''
        parse golem item data from the save buffer
        '''
        if Character(self._buffer).character_class != CharacterClass.NECROMANCER:
            return ptr

        gcount = self._buffer[ptr]
        ptr += 1

        if gcount == 1:
            item = Item.from_data(self._buffer, ptr)
            ptr += item.length
            self._gdata.append(item)

        return ptr

    @property
    def _header(self):
        '''
        produce the header of the items section - should be 'JM'
        '''
        if self._buffer.sparse:
            return 'JM'
        return self._buffer[self._offset:self._offset + 2].decode('ascii')

    @property
    def pdata(self):
        '''
        get the player item data
        '''
        return self._pdata

    @property
    def cdata(self):
        '''
        get the player corpse item data
        '''
        return self._cdata

    @property
    def mdata(self):
        '''
        get the mercenary item data
        '''
        return self._mdata

    @property
    def gdata(self):
        '''
        get the iron golem item data
        '''
        return self._gdata
