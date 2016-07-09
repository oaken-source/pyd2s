
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

        if self.file_magic != 0xaa55aa55:
            raise ValueError('invalid save file - mismatched magic number')
        if self.file_version != 0x60:
            raise NotImplementedError('File Version %#x not supported' % version)

    @property
    def file_magic(self):
        return struct.unpack('<L', self._buffer[0:4])[0]

    @property
    def file_version(self):
        return struct.unpack('<L', self._buffer[4:8])[0]

    @property
    def file_size(self):
        return struct.unpack('<L', self._buffer[8:12])[0]

    @property
    def file_checksum(self):
        return struct.unpack('<L', self._buffer[12:16])[0]

    @property
    def active_arms(self):
        return struct.unpack('<L', self._buffer[16:20])[0]

    @property
    def name(self):
        return self._buffer[20:36].decode('utf-8').rstrip('\0')

    @property
    def expansion_character(self):
        return (self._buffer[36] & (1 << 5)) != 0

    @property
    def died(self):
        return (self._buffer[36] & (1 << 3)) != 0

    @property
    def hardcore(self):
        return (self._buffer[36] & (1 << 2)) != 0

    @property
    def progression(self):
        return self._buffer[37]

    @property
    def character_class(self):
        return self._buffer[40]

    @property
    def character_level(self):
        return self._buffer[43]

    @property
    def timestamp(self):
        return struct.unpack('<L', self._buffer[48:52])

    @property
    def skill_hotkeys(self):
        return struct.unpack('<16L', self._buffer[56:120])

    @property
    def skill_leftclick(self):
        return struct.unpack('<L', self._buffer[120:124])[0]

    @property
    def skill_rightclick(self):
        return struct.unpack('<L', self._buffer[124:128])[0]

    @property
    def skill_alt_leftclick(self):
        return struct.unpack('<L', self._buffer[128:132])[0]

    @property
    def skill_alt_rightclick(self):
        return struct.unpack('<L', self._buffer[132:136])[0]

    @property
    def played_difficulty(self):
        return 0 if self._buffer[168] else 1 if self._buffer[169] else 2

    @property
    def played_act(self):
        return self._buffer[168 + self.played_difficulty] & 0x3

    @property
    def map_id(self):
        return struct.unpack('<L', self._buffer[171:175])[0]

    @property
    def mercenary_dead(self):
        return struct.unpack('<H', self._buffer[177:179])[0] != 0

    @property
    def mercenary_id(self):
        return struct.unpack('<L', self._buffer[179:183])[0]

    @property
    def mercenary_name_id(self):
        return struct.unpack('<H', self._buffer[183:185])[0]

    @property
    def mercenary_attributes(self):
        return struct.unpack('<H', self._buffer[185:187])[0]

    @property
    def mercenary_experience(self):
        return struct.unpack('<L', self._buffer[187:191])[0]
