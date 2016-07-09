
'''
This module provides classes to manage D2 save games.
'''

import struct

class D2Save(object):
    '''
    This class represents an instance of a D2 save file.
    '''

    @classmethod
    def from_file(cls, filename):
        '''
        read save data from a file
        '''
        with open(filename, 'rb') as d2sfile:
            return cls.from_bytes(d2sfile.read())

    @classmethod
    def from_bytes(cls, buffer):
        '''
        read save data from a buffer of bytes
        '''
        if len(buffer) < 334:
            raise ValueError('invalid save file - too short')
        magic, version, size, checksum = struct.unpack('<LLLL', buffer[0:16])
        if magic != 0xaa55aa55:
            raise ValueError('invalid save file - mismatched magic number')
        if version != 0x60:
            raise NotImplementedError('File Version %#x not supported' % version)
