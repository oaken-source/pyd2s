
'''
this module provides a class that manages character data
'''

import struct

from pyd2s.basictypes import CharacterClass, Difficulty, Act


class Character(object):
    '''
    save data referring to the character itself
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
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
        return CharacterClass(self._buffer[40])

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
            return Difficulty.Normal
        if self._buffer[169]:
            return Difficulty.Nightmare
        return Difficulty.Hell

    @property
    def current_act(self):
        '''
        the last played act
        '''
        return Act(self._buffer[168 + self.current_difficulty.value] & 0x3)

    @property
    def map_seed(self):
        '''
        the map generation seed
        '''
        return struct.unpack('<L', self._buffer[171:175])[0]


