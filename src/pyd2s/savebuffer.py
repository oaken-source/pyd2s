
'''
this module provides a change-aware buffer for d2s files
'''

import os
import struct
import logging
import datetime


class SaveBuffer(bytearray):
    '''
    manage the buffer of a save file and maintain its checksum
    '''
    class BitPointer:
        '''
        a self-advancing bit-wise read pointer
        '''
        def __init__(self, buffer, offset):
            '''
            constructor
            '''
            self._buffer = buffer
            self._start = offset
            self._pos = offset

        def read(self, length):
            '''
            read the next length bits and return as integer, advancing the pointer
            '''
            res = self._buffer.getbits(self._pos, length)
            self._pos += length
            return res

        def write(self, length, value):
            '''
            overwrite the next length bits with the given integer, advancing the pointer
            '''
            self._buffer.setbits(self._pos, value, length)
            self._pos += length

        def read_string(self):
            '''
            read a 7-bit ascii null-terminated string from the buffer
            '''
            res = bytearray()
            while True:
                next_char = self.read(7)
                if next_char == 0:
                    break
                res.append(next_char)
            return res.decode('ascii')

        @property
        def value(self):
            '''
            the current value of the pointer
            '''
            return self._pos

        @property
        def distance(self):
            '''
            the distance the pointer has travelled in bits
            '''
            return self._pos - self._start

    class DynamicOffset:
        '''
        an offset into the save buffer that is kept around and updated when necessary
        '''
        def __init__(self, offset):
            '''
            constructor
            '''
            self._offset = offset

        def __add__(self, other):
            '''
            add to the offset
            '''
            return int(self) + int(other)

        def __sub__(self, other):
            '''
            subtract from the offset
            '''
            return int(self) - int(other)

        def __mul__(self, other):
            '''
            multiply the offset
            '''
            return int(self) * int(other)

        def __index__(self):
            '''
            use the offset as an index
            '''
            return self._offset

        def __ge__(self, other):
            '''
            enable integer comparison
            '''
            if self.__class__ is other.__class__:
                return self._offset >= other._offset
            return self._offset >= other

        def adjust_by(self, value):
            '''
            adjust the dynamic offset in the buffer
            '''
            self._offset += value

    @classmethod
    def open(cls, path):
        '''
        read the input file into memory
        '''
        with open(path, 'rb') as save:
            res = cls(save.read())
        res._path = path
        return res

    def __init__(self, data):
        '''
        constructor
        '''
        super().__init__(data)

        self._path = None
        self._dynamic_offsets = []

    @property
    def _size(self):
        '''
        get the size of the save file in bytes
        '''
        return struct.unpack_from('<L', self, 0x08)[0]

    @_size.setter
    def _size(self, value):
        '''
        set the size of the save file in bytes
        '''
        struct.pack_into('<L', self, 0x08, value)

    @property
    def path(self):
        '''
        produce the path to the save file
        '''
        return self._path

    def dynamic_offset(self, offset):
        '''
        produce a dynamic reference to an offset into the buffer
        '''
        res = self.DynamicOffset(offset)
        self._dynamic_offsets.append(res)
        return res

    def remove_dynamic_offset(self, offset):
        '''
        stop tracking the given offset
        '''
        self._dynamic_offsets.remove(offset)

    def bit_pointer(self, offset):
        '''
        produce a bit pointer into the buffer
        '''
        return self.BitPointer(self, offset)

    def insert_bytes(self, start, length):
        '''
        insert the given number of zero bytes in the buffer
        '''
        logging.debug('SaveBuffer:inserting %d bytes at %d', length, start)
        self[start:start] = [0] * length

        # update the dynamic offsets
        for offset in self._dynamic_offsets:
            if offset >= start:
                offset.adjust_by(length)

    def remove_bytes(self, start, length):
        '''
        take the given number of bytes from the buffer
        '''
        logging.debug('SaveBuffer:removing %d bytes at %d', length, start)
        self[start:start + length] = []

        # update the dynamic offsets
        for offset in self._dynamic_offsets:
            if offset >= start:
                offset.adjust_by(-length)

    def getbits(self, start, length):
        '''
        produce an integer from the given bit position and length
        '''
        res = 0
        for i in range(length):
            pos = start + i
            res |= ((self[pos >> 3] & (1 << (pos & 0x07))) != 0) << i
        return res

    def setbits(self, start, value, length):
        '''
        set the given bits to the given value
        '''
        for i in range(length):
            pos = start + i
            self[pos >> 3] ^= (-((value >> i) & 0x1) ^ self[pos >> 3]) & (1 << (pos & 0x07))

    def flush(self, backup=False):
        '''
        write the changed data back to disk, with optional backup
        '''
        if backup:
            mtime = os.path.getmtime(self._path)
            timestamp = datetime.datetime.fromtimestamp(mtime).strftime("%Y%m%d-%H%M%S")
            os.rename(self._path, self._path + "_" + timestamp)

        with open(self._path, 'wb') as save:
            save.write(self)
