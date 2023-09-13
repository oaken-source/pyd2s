'''
this module provides classes specific to PlugY stash data
'''

import struct
from enum import Enum

from pyd2s.item import Item
from pyd2s.itemlocation import ItemMap
from pyd2s.savebuffer import SaveBuffer


class PlugyStashPage:
    '''
    a page of data in a plugy stash
    '''
    class Flags(Enum):
        '''
        the flags on the page
        '''
        SHARED = 1
        INDEX = 2
        MAIN_INDEX = 4
        RESERVED = 8

    def __init__(self, buffer, offset):
        '''
        parse a page of plugy data from the buffer
        '''
        self._buffer = buffer
        self._offset = buffer.dynamic_offset(offset)

        if self.header != 'ST':
            raise ValueError(f'invalid save: mismatched page header: {self.header}')

        ptr = offset + 6 + len(self.name) + 1
        if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
            raise ValueError('invalid save: mismatched item data section header')
        ptr += 2

        self._icount = buffer.dynamic_offset(ptr)
        ptr += 2

        idata = []
        for _ in range(self.icount):
            item = Item.from_data(self._buffer, ptr)
            ptr += item.length
            idata.append(item)

        self._end = buffer.dynamic_offset(ptr)

        self._imap = ItemMap(10, 10, idata)

    @property
    def header(self):
        '''
        the header of the page. must be ST
        '''
        return self._buffer[self._offset:self._offset + 2].decode('ascii')

    @property
    def flags(self):
        '''
        the flags of the page
        '''
        return struct.unpack_from('<L', self._buffer, self._offset + 2)[0]

    @flags.setter
    def flags(self, value):
        '''
        set the flags on the page
        '''
        struct.pack_into('<L', self._buffer, self._offset + 2, value)

    @property
    def name(self):
        '''
        the name of the page
        '''
        ptr = self._offset + 6

        name = bytearray()
        while True:
            char = self._buffer[ptr]
            ptr += 1
            if char == 0:
                break
            name.append(char)
        return name.decode('ascii')

    @property
    def length(self):
        '''
        produce the length of the page in bytes
        '''
        return self._end - self._offset

    @property
    def icount(self):
        '''
        the item count of the page
        '''
        return struct.unpack_from('<H', self._buffer, self._icount)[0]

    @icount.setter
    def icount(self, value):
        '''
        set the item count of the page
        '''
        struct.pack_into('<H', self._buffer, self._offset + 9, value)

    @property
    def idata(self):
        '''
        produce the item data of the stash page
        '''
        return self._imap.items

    @property
    def imap(self):
        '''
        produce an inventory map of the stash page
        '''
        return self._imap

    def take(self, item):
        '''
        remove an item from the stash and return it with its own raw buffer
        '''
        # remove from the itemlist
        self._imap.take(item)

        # update the item count
        self.icount -= 1

        # detach the item from the page
        item.detach()

        return item

    def put(self, item):
        '''
        add an item to the stash page, without checking position
        '''
        # attach to the buffer
        item.attach(self._buffer, int(self._end))

        # add to the itemlist
        self._imap.put(item)

        # update the item count
        self.icount += 1

    @property
    def raw_data(self):
        '''
        the raw data of the plugy page
        '''
        return self._buffer[self._offset:self._end]

    def detach(self):
        '''
        replace the parent buffer with a new one containing this pages rawdata
        '''
        # remove all items
        items = []
        while self.idata:
            items.append(self.take(self.idata[0]))

        # detach the buffer
        new_buffer = SaveBuffer(self.raw_data)
        self._buffer.remove_dynamic_offset(self._offset)
        self._buffer.remove_dynamic_offset(self._icount)
        self._buffer.remove_dynamic_offset(self._end)
        self._buffer.remove_bytes(self._offset, self.length)
        self._buffer = new_buffer
        self._offset = 0

        # add all items back again
        for item in items:
            self.put(item)
