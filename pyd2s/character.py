
'''
this module provides a class that manages character data
'''

import struct

from pyd2s.basictypes import CharacterClass, Difficulty, Act
from pyd2s.statdata import StatData


class Character(object):
    '''
    save data referring to the character itself
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        self._statdata = StatData(self._buffer)

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
    def _progression(self):
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

    @property
    def strength(self):
        '''
        the characters strength
        '''
        return self._statdata.strength

    @property
    def energy(self):
        '''
        the characters energy
        '''
        return self._statdata.energy

    @property
    def dexterity(self):
        '''
        the characters dexterity
        '''
        return self._statdata.dexterity

    @property
    def vitality(self):
        '''
        the characters vitality
        '''
        return self._statdata.vitality

    @property
    def statpts(self):
        '''
        the characters unassigned stat points
        '''
        return self._statdata.statpts

    @property
    def newskills(self):
        '''
        the characters unassigned skill points
        '''
        return self._statdata.newskills

    @property
    def hitpoints(self):
        '''
        the characters current hit points
        '''
        return self._statdata.hitpoints

    @property
    def maxhp(self):
        '''
        the characters maximum hitpoints
        '''
        return self._statdata.maxhp

    @property
    def mana(self):
        '''
        the characters current mana points
        '''
        return self._statdata.mana

    @property
    def maxmana(self):
        '''
        the characters maximum mana points
        '''
        return self._statdata.maxmana

    @property
    def stamina(self):
        '''
        the characters current stamina points
        '''
        return self._statdata.stamina

    @property
    def maxstamina(self):
        '''
        the characters maximum stamina points
        '''
        return self._statdata.maxstamina

    @property
    def experience(self):
        '''
        the characters current experience points
        '''
        return self._statdata.experience

    @property
    def gold(self):
        '''
        the characters current gold
        '''
        return self._statdata.gold

    @property
    def goldbank(self):
        '''
        the characters current gold in the stash
        '''
        return self._statdata.goldbank
