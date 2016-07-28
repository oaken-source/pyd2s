
'''
this module provides a class that manages character data
'''

import re
from os.path import dirname, join, isfile

from pyd2s.basictypes import CharacterClass
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

        #self._statdata = StatData(self._buffer)

    @property
    def name(self):
        '''
        get the name of the character
        '''
        return self._buffer[20:36].decode('ascii').rstrip('\0')

    @name.setter
    def name(self, value):
        '''
        set the name of the character, this also updates save file locations
        '''
        if value == self.name:
            return

        if not re.fullmatch('(?=.{2,15})[a-zA-Z]+[-_]?[a-zA-Z]+', value):
            raise ValueError('character name is invalid')

        newpath = join(dirname(self._buffer.path), "%s.d2s" % value)
        if isfile(newpath):
            raise ValueError('a character with this name already exists')

        self._buffer.path = newpath
        self._buffer[20:36] = value.ljust(16, '\0').encode('ascii')

    @property
    def is_ladder(self):
        '''
        True if the character is in the ladder, False otherwise
        '''
        return (self._buffer[36] & (1 << 6)) != 0

    @is_ladder.setter
    def is_ladder(self, value):
        '''
        set wether the character is in the ladder
        '''
        self._buffer[36] ^= (-bool(value) ^ self._buffer[36]) & (1 << 6)

    @property
    def is_expansion(self):
        '''
        True if an extension (LoD) character, False otherwise
        '''
        return (self._buffer[36] & (1 << 5)) != 0

    @is_expansion.setter
    def is_expansion(self, value):
        '''
        set wether the character is in the expansion
        '''
        if not value and self.character_class in (CharacterClass.Assassin, CharacterClass.Druid):
            raise ValueError('assassins and druids need expansion flag set')
        self._buffer[36] ^= (-bool(value) ^ self._buffer[36]) & (1 << 5)

    @property
    def has_died(self):
        '''
        True if the character has died in the past, False otherwise
        '''
        return (self._buffer[36] & (1 << 3)) != 0

    @has_died.setter
    def has_died(self, value):
        '''
        set wether the character has died in the past
        '''
        self._buffer[36] ^= (-bool(value) ^ self._buffer[36]) & (1 << 3)

    @property
    def is_hardcore(self):
        '''
        True if the character is a hardcore character, False otherwise
        '''
        return (self._buffer[36] & (1 << 2)) != 0

    @is_hardcore.setter
    def is_hardcore(self, value):
        '''
        set wether the character is a hardcore character
        '''
        self._buffer[36] ^= (-bool(value) ^ self._buffer[36]) & (1 << 2)

    @property
    def character_class(self):
        '''
        get the class of the character
        '''
        return CharacterClass(self._buffer[40])

    @character_class.setter
    def character_class(self, value):
        '''
        set the class of the character
        '''
        if not isinstance(value, CharacterClass):
            raise ValueError('character class is invalid')
        if value in (CharacterClass.Assassin, CharacterClass.Druid):
            self.is_expansion = True
        self._buffer[40] = value.value

    @property
    def level(self):
        '''
        get the current level of the character
        '''
        return self._buffer[43]

    @level.setter
    def level(self, value):
        '''
        set the current level of the character
        '''
        if not 0 < value < 100:
            raise ValueError('character level is invalid')
        self._buffer[43] = value
        raise NotImplementedError('todo: update level and experience in stats section')

    # @property
    # def strength(self):
    #     '''
    #     the characters strength
    #     '''
    #     return self._statdata.strength

    # @property
    # def energy(self):
    #     '''
    #     the characters energy
    #     '''
    #     return self._statdata.energy

    # @property
    # def dexterity(self):
    #     '''
    #     the characters dexterity
    #     '''
    #     return self._statdata.dexterity

    # @property
    # def vitality(self):
    #     '''
    #     the characters vitality
    #     '''
    #     return self._statdata.vitality

    # @property
    # def statpts(self):
    #     '''
    #     the characters unassigned stat points
    #     '''
    #     return self._statdata.statpts

    # @property
    # def newskills(self):
    #     '''
    #     the characters unassigned skill points
    #     '''
    #     return self._statdata.newskills

    # @property
    # def hitpoints(self):
    #     '''
    #     the characters current hit points
    #     '''
    #     return self._statdata.hitpoints

    # @property
    # def maxhp(self):
    #     '''
    #     the characters maximum hitpoints
    #     '''
    #     return self._statdata.maxhp

    # @property
    # def mana(self):
    #     '''
    #     the characters current mana points
    #     '''
    #     return self._statdata.mana

    # @property
    # def maxmana(self):
    #     '''
    #     the characters maximum mana points
    #     '''
    #     return self._statdata.maxmana

    # @property
    # def stamina(self):
    #     '''
    #     the characters current stamina points
    #     '''
    #     return self._statdata.stamina

    # @property
    # def maxstamina(self):
    #     '''
    #     the characters maximum stamina points
    #     '''
    #     return self._statdata.maxstamina

    # @property
    # def experience(self):
    #     '''
    #     the characters current experience points
    #     '''
    #     return self._statdata.experience

    # @property
    # def gold(self):
    #     '''
    #     the characters current gold
    #     '''
    #     return self._statdata.gold

    # @property
    # def goldbank(self):
    #     '''
    #     the characters current gold in the stash
    #     '''
    #     return self._statdata.goldbank
