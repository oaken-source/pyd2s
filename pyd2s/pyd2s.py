
'''
This module provides classes to manage D2 save games.
'''

import os
import mmap
import struct


class D2SaveFile(object):

    def __init__(self, path):
        self.path = path
        self._fd = os.open(path, os.O_RDWR)
        self._buffer = mmap.mmap(self._fd, 0)

        if self._magic != 0xaa55aa55:
            raise ValueError('invalid save file')
        if self.version != 0x60:
            raise NotImplementedError('File Version %#x not supported' % self.version)

        self.character = D2SaveCharacter(self, self._buffer)
        self.mercenary = D2SaveMercenary(self, self._buffer)

    @property
    def _magic(self):
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
    def timestamp(self):
        return struct.unpack('<L', self._buffer[48:52])


class D2SaveCharacter(object):

    def __init__(self, d2s, buffer):
        self._d2s = d2s
        self._buffer = buffer

    @property
    def active_arms(self):
        return struct.unpack('<L', self._buffer[16:20])[0]

    @property
    def name(self):
        return self._buffer[20:36].decode('ascii').rstrip('\0')

    @property
    def is_ladder(self):
        return (self._buffer[36] & (1 << 6)) != 0

    @property
    def is_expansion(self):
        return (self._buffer[36] & (1 << 5)) != 0

    @property
    def has_died(self):
        return (self._buffer[36] & (1 << 3)) != 0

    @property
    def is_hardcore(self):
        return (self._buffer[36] & (1 << 2)) != 0

    @property
    def progression(self):
        return self._buffer[37]

    @property
    def character_class(self):
        return self._buffer[40]

    @property
    def level(self):
        return self._buffer[43]

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
    def current_difficulty(self):
        return 0 if self._buffer[168] else 1 if self._buffer[169] else 2

    @property
    def current_act(self):
        return self._buffer[168 + self.current_difficulty] & 0x3

    @property
    def map_id(self):
        return struct.unpack('<L', self._buffer[171:175])[0]


class D2SaveMercenary(object):

    def __init__(self, d2s, buffer):
        self._d2s = d2s
        self._buffer = buffer

    @property
    def is_dead(self):
        return struct.unpack('<H', self._buffer[177:179])[0] != 0

    @property
    def control_seed(self):
        return struct.unpack('<L', self._buffer[179:183])[0]

    @property
    def name_id(self):
        return struct.unpack('<H', self._buffer[183:185])[0]

    @property
    def type(self):
        return struct.unpack('<H', self._buffer[185:187])[0]

    @property
    def experience(self):
        return struct.unpack('<L', self._buffer[187:191])[0]
