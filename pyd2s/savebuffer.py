
'''
this module provides a change-aware buffer for d2s files
'''

import glob
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
        return struct.unpack_from('<L', self, 8)[0]

    @_size.setter
    def _size(self, value):
        '''
        set the size of the save file in bytes
        '''
        struct.pack_into('<L', self, 8, value)

    @property
    def _checksum(self):
        '''
        get the checksum of the save data
        '''
        return struct.unpack_from('<L', self, 12)[0]

    @_checksum.setter
    def _checksum(self, value):
        '''
        set the checksum of the save data
        '''
        struct.pack_into('<L', self, 12, value)

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
            position = start + i
            res |= ((self[position >> 3] & (1 << (position & 0x07))) != 0) << i
        return res

    def setbits(self, position, value, length):
        '''
        todo
        '''
        pass

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
