
'''
this module provides a change-aware buffer for d2s files
'''

import glob
import struct
import logging
from os import rename
from os.path import dirname, basename, join


class SaveBuffer(bytearray):
    '''
    manage the buffer of a save file and maintain its checksum
    '''
    class BitReadPointer:
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

        def read_bits(self, length):
            '''
            read the next length bits and return as integer, advancing the pointer
            '''
            res = self._buffer.getbits(self._pos, length)
            self._pos += length
            return res

        def read_string(self):
            '''
            read a 7-bit ascii null-terminated string from the buffer
            '''
            res = bytearray()
            while True:
                next_char = self.read_bits(7)
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
            return self._offset + other

        def __mul__(self, other):
            '''
            multiply the offset
            '''
            return self._offset * other

        def __index__(self):
            '''
            use the offset as an index
            '''
            return self._offset

        def __ge__(self, other):
            '''
            enable integer comparison
            '''
            return self._offset >= other

        def adjust_by(self, value):
            '''
            adjust the dynamic offset in the buffer
            '''
            self._offset += value

    def __init__(self, path):
        '''
        constructor - read the input file into memory
        '''
        self._path = path
        self._newpath = None
        self._dynamic_offsets = []

        with open(path, 'rb') as save:
            super().__init__(save.read())

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
    def sparse(self):
        '''
        indicate whether the save file in sparse (has never been saved in-game)
        '''
        return len(self) <= 335

    @property
    def _checksum(self):
        '''
        get the checksum of the save data
        '''
        return struct.unpack_from('<L', self, 0x0c)[0]

    @_checksum.setter
    def _checksum(self, value):
        '''
        set the checksum of the save data
        '''
        struct.pack_into('<L', self, 0x0c, value)

    @property
    def path(self):
        '''
        produce the path to the save file
        '''
        return self._path

    @path.setter
    def path(self, value):
        '''
        set the new path to the save file - move on flush
        '''
        self._newpath = value

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

    def dynamic_offset(self, offset):
        '''
        produce a dynamic reference to an offset into the buffer
        '''
        res = self.DynamicOffset(offset)
        self._dynamic_offsets.append(res)
        return res

    def flush(self):
        '''
        write the changed data back to disk
        '''
        # move the character files, if the path has been changed
        if self._newpath is not None:
            oldprefix = join(dirname(self._path), basename(self._path).partition('.')[0])
            newprefix = join(dirname(self._newpath), basename(self._newpath).partition('.')[0])
            extensions = ['.' + basename(f).partition('.')[2] for f in glob.glob(oldprefix + '.*')]
            for extension in extensions:
                rename(oldprefix + extension, newprefix + extension)

            self._path, self._newpath = self._newpath, None

        # update size and checksum
        self._size = len(self)
        self._checksum = 0

        checksum = 0
        for byte in self:
            checksum = (((checksum << 1) | (checksum & 0x80000000 > 0)) + byte) & 0xffffffff
        self._checksum = checksum

        # write back
        with open(self._path, 'wb') as save:
            save.write(self)
