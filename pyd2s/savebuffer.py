
'''
this module provides a change-aware buffer for d2s files
'''

import struct


class SaveBuffer(object):
    '''
    manage the buffer of a save file and maintain its checksum
    '''

    def __init__(self, path):
        '''
        constructor - read the input file into memory
        '''
        self._path = path
        with open(path, 'rb') as save:
            self._buffer = save.read()

        self._dirty = False

    @property
    def size(self):
        '''
        the size of the save file in bytes
        '''
        return struct.unpack('<L', self[8:12])[0]

    @property
    def checksum(self):
        '''
        the checksum of the save data - automatically maintained
        '''
        return struct.unpack('<L', self[12:16])[0]

    @property
    def timestamp(self):
        '''
        the last save timestamp
        '''
        return struct.unpack('<L', self[48:52])

    def __getitem__(self, key):
        '''
        produce an item or a slice of the underlying buffer
        '''
        return self._buffer[key]

    def __setitem__(self, key, value):
        '''
        propagate changes to the underlying buffer and set the dirty flag
        '''
        self._dirty = True
        self._buffer[key] = value
