
'''
This module provides classes to manage D2 save games.
'''

import os
import mmap
import struct

class D2Save(object):
    '''
    This class represents an instance of a D2 save file.
    '''

    def __init__(self, filename):
        self._filename = filename
        self._fd = os.open(filename, os.O_RDWR)
        self._buffer = mmap.mmap(self._fd, 0)

        if self.magic != 0xaa55aa55:
            raise ValueError('invalid save file - mismatched magic number')
        if self.version != 0x60:
            raise NotImplementedError('File Version %#x not supported' % version)

        print('magic:    %#x' % self.magic)
        print('version:  %#x' % self.version)
        print('size:     %i' % self.size)
        print('checksum: %#x' % self.checksum)
        print('name:     %s' % self.name)

    @property
    def magic(self):
        return struct.unpack('<L', self._buffer[0:4])[0]

    @property
    def version(self):
        return struct.unpack('<L', self._buffer[4:8])[0]

    @property
    def size(self):
        return struct.unpack('<L', self._buffer[8:12])[0]

    @property
    def checksum(self):
        return struct.unpack('<L', self._buffer[12:16])[0]

    @property
    def name(self):
        return self._buffer[20:36].decode('utf-8').rstrip('\0')
