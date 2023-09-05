'''
this module provides classes specific to PlugY stash data
'''

import struct

from pyd2s.item import Item


class PlugyStashPage:
    '''
    a page of data in a plugy stash
    '''
    def __init__(self, buffer, offset):
        '''
        parse a page of plugy data from the buffer
        '''
        self._buffer = buffer
        self._offset = offset

        if self.header != 'ST':
            raise ValueError('invalid save: mismatched page header')

        ptr = offset + 2

        self._flags = struct.unpack_from('<L', self._buffer, ptr)
        ptr += 4

        name = bytearray()
        while True:
            char = self._buffer[ptr]
            ptr += 1
            if char == 0:
                break
            name.append(char)
        self._name = name.decode('ascii')

        if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
            raise ValueError('invalid save: mismatched item data section header')
        ptr += 2

        self._idata = []
        icount = struct.unpack_from('<H', self._buffer, ptr)[0]
        ptr += 2

        for _ in range(icount):
            item = Item.from_data(self._buffer, ptr)
            ptr += item.length
            self._idata.append(item)

        self._length = ptr - offset

    @property
    def header(self):
        '''
        the header of the page. must be ST
        '''
        return self._buffer[self._offset:self._offset + 2].decode('ascii')

    @property
    def length(self):
        '''
        produce the length of the page in bytes
        '''
        return self._length

    @property
    def name(self):
        '''
        the name of the page
        '''
        return self._name

    @property
    def idata(self):
        '''
        produce the item data of the stash page
        '''
        return self._idata
