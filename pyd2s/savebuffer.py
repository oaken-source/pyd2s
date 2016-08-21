
'''
this module provides a change-aware buffer for d2s files
'''

import glob
import math
import struct
from os import rename
from os.path import dirname, basename, join


class SaveBuffer(bytearray):
    '''
    manage the buffer of a save file and maintain its checksum
    '''

    def __init__(self, path):
        '''
        constructor - read the input file into memory
        '''
        self._path = path
        self._newpath = None

        with open(path, 'rb') as save:
            super(SaveBuffer, self).__init__(save.read())

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

    def addbits(self, start, length, align_at):
        '''
        add the given bits to the given position, keeping the byte-alignment intact
        '''
        byte = math.ceil(align_at / 8.0)
        fill = (math.ceil((align_at + length) / 8.0) - byte) * [0]
        self[byte:byte] = fill
        self.setbits(start + length, self.getbits(start, align_at - start), align_at - start)

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
