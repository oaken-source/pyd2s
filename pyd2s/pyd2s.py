
'''
This module provides classes to manage D2 save games.
'''

import os
import mmap
import struct
from enum import Enum


class D2CharacterClass(Enum):
    '''
    the character classes available in the game
    '''
    Amazon = 0x00
    Sorceress = 0x01
    Necromancer = 0x02
    Paladin = 0x03
    Barbarian = 0x04
    Druid = 0x05
    Assassin = 0x06


class D2Difficulty(Enum):
    '''
    the difficulty levels available in the game
    '''
    Normal = 0x00
    Nightmare = 0x01
    Hell = 0x02


class D2Act(Enum):
    '''
    the acts available in the game
    '''
    Act1 = 0x00
    Act2 = 0x01
    Act3 = 0x02
    Act4 = 0x03
    Act5 = 0x04


class D2SaveFile(object):
    '''
    a .d2s file containing diablo 2 save game data
    '''

    def __init__(self, path):
        '''
        constructor - mmap file data and do sanity checks
        '''
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
        '''
        the magic number of d2s files - should be 0xaa55aa55
        '''
        return struct.unpack('<L', self._buffer[0:4])[0]

    @property
    def version(self):
        '''
        the version of the file - supported values are 0x60 for >=1.10
        '''
        return struct.unpack('<L', self._buffer[4:8])[0]

    @property
    def size(self):
        '''
        the size of the save file in bytes
        '''
        return struct.unpack('<L', self._buffer[8:12])[0]

    @property
    def _checksum(self):
        '''
        the checksum of the save data - automatically maintained
        '''
        return struct.unpack('<L', self._buffer[12:16])[0]

    @property
    def timestamp(self):
        '''
        the last save timestamp
        '''
        return struct.unpack('<L', self._buffer[48:52])


class D2SaveCharacter(object):
    '''
    save data referring to the character itself
    '''

    def __init__(self, d2s, buffer):
        '''
        constructor - propagate parent structure and buffer
        '''
        self._d2s = d2s
        self._buffer = buffer

    @property
    def active_arms(self):
        '''
        the number of the currently active weapon set of the character
        '''
        return struct.unpack('<L', self._buffer[16:20])[0]

    @property
    def name(self):
        '''
        the name of the character
        '''
        return self._buffer[20:36].decode('ascii').rstrip('\0')

    @property
    def is_ladder(self):
        '''
        True if the character is in the ladder, False otherwise
        '''
        return (self._buffer[36] & (1 << 6)) != 0

    @property
    def is_expansion(self):
        '''
        True if an extension (LoD) character, False otherwise
        '''
        return (self._buffer[36] & (1 << 5)) != 0

    @property
    def has_died(self):
        '''
        True if the character has died in the past, False otherwise
        '''
        return (self._buffer[36] & (1 << 3)) != 0

    @property
    def is_hardcore(self):
        '''
        True if the character is a hardcore character, False otherwise
        '''
        return (self._buffer[36] & (1 << 2)) != 0

    @property
    def progression(self):
        '''
        an integer representing the characters progress in the game and its title
        '''
        return self._buffer[37]

    @property
    def character_class(self):
        '''
        the class of the character
        '''
        return D2CharacterClass(self._buffer[40])

    @property
    def level(self):
        '''
        the current level of the character
        '''
        return self._buffer[43]

    @property
    def skill_hotkeys(self):
        '''
        the list of assigned skills to the 16 hot keys
        '''
        return struct.unpack('<16L', self._buffer[56:120])

    @property
    def skill_leftclick(self):
        '''
        the skill assigned to left click of weapon set 1
        '''
        return struct.unpack('<L', self._buffer[120:124])[0]

    @property
    def skill_rightclick(self):
        '''
        the skill assigned to right click of weapon set 1
        '''
        return struct.unpack('<L', self._buffer[124:128])[0]

    @property
    def skill_alt_leftclick(self):
        '''
        the skill assigned to left click of weapon set 2
        '''
        return struct.unpack('<L', self._buffer[128:132])[0]

    @property
    def skill_alt_rightclick(self):
        '''
        the skill assigned to right click of weapon set 2
        '''
        return struct.unpack('<L', self._buffer[132:136])[0]

    @property
    def current_difficulty(self):
        '''
        the last played difficulty
        '''
        if self._buffer[168]:
            return D2Difficulty.Normal
        if self._buffer[169]:
            return D2Difficulty.Nightmare
        return D2Difficulty.Hell

    @property
    def current_act(self):
        '''
        the last played act
        '''
        return D2Act(self._buffer[168 + self.current_difficulty] & 0x3)

    @property
    def map_seed(self):
        '''
        the map generation seed
        '''
        return struct.unpack('<L', self._buffer[171:175])[0]


class D2SaveMercenary(object):
    '''
    save data referring to the characters mercenary
    '''

    def __init__(self, d2s, buffer):
        '''
        constructor - propagate parent structure and buffer
        '''
        self._d2s = d2s
        self._buffer = buffer

    @property
    def is_dead(self):
        '''
        True if the mercenary is currently dead, False otherwise
        '''
        return struct.unpack('<H', self._buffer[177:179])[0] != 0

    @property
    def control_seed(self):
        '''
        the mercenary control seed
        '''
        return struct.unpack('<L', self._buffer[179:183])[0]

    @property
    def name_id(self):
        '''
        the id into the language dependent mercenary name table
        '''
        return struct.unpack('<H', self._buffer[183:185])[0]

    @property
    def type(self):
        '''
        the type of the active mercenary - encodes act and capabilities
        '''
        return struct.unpack('<H', self._buffer[185:187])[0]

    @property
    def experience(self):
        '''
        the experience points of the active mercenary
        '''
        return struct.unpack('<L', self._buffer[187:191])[0]
