
'''
this module provides a change-aware buffer for d2s files
'''

import time
import struct


class SaveBuffer(bytearray):
    '''
    manage the buffer of a save file and maintain its checksum
    '''

    def __init__(self, path):
        '''
        constructor - read the input file into memory
        '''
        self._path = path
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
    def _timestamp(self):
        '''
        get the last save timestamp
        '''
        return struct.unpack_from('<L', self, 48)[0]

    @_timestamp.setter
    def _timestamp(self, value):
        '''
        set the last save timestamp
        '''
        struct.pack_into('<L', self, 48, value)

    def flush(self):
        '''
        write the changed data back to disk
        '''
        self._size = len(self)
        self._timestamp = int(time.time())
        self._checksum = 0

        checksum = 0
        for byte in self:
            checksum = (((checksum << 1) | (checksum & 0x80000000 > 0)) + byte) & 0xffffffff

        self._checksum = checksum

        with open(self._path, 'wb') as save:
            save.write(self)
