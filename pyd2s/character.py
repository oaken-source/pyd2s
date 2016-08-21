
'''
this module provides a class that manages character data
'''

import re
from os.path import dirname, join, isfile

from pyd2s.statdata import Stats, StatData
from pyd2s.basictypes import CharacterClass


class Character(object):
    '''
    save data referring to the character itself
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        self._stats = StatData(self._buffer)

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
        self._stats.set(Stats.level, value)

    @property
    def strength(self):
        '''
        the characters strength
        '''
        return self._stats.get(Stats.strength)

    @strength.setter
    def strength(self, value):
        '''
        set the characters strength
        '''
        self._stats.set(Stats.strength, value)

    @property
    def energy(self):
        '''
        the characters energy
        '''
        return self._stats.get(Stats.energy)

    @energy.setter
    def energy(self, value):
        '''
        set the characters energy
        '''
        self._stats.set(Stats.energy, value)

    @property
    def dexterity(self):
        '''
        the characters dexterity
        '''
        return self._stats.get(Stats.dexterity)

    @dexterity.setter
    def dexterity(self, value):
        '''
        set the characters dexterity
        '''
        self._stats.set(Stats.dexterity, value)

    @property
    def vitality(self):
        '''
        the characters vitality
        '''
        return self._stats.get(Stats.vitality)

    @vitality.setter
    def vitality(self, value):
        '''
        set the characters vitality
        '''
        self._stats.set(Stats.vitality, value)

    @property
    def statpts(self):
        '''
        the characters unassigned stat points
        '''
        return self._stats.get(Stats.statpts)

    @statpts.setter
    def statpts(self, value):
        '''
        set the characters unassigned stat points
        '''
        self._stats.set(Stats.statpts, value)

    @property
    def newskills(self):
        '''
        the characters unassigned skill points
        '''
        return self._stats.get(Stats.newskills)

    @newskills.setter
    def newskills(self, value):
        '''
        set the characters unassigned skill points
        '''
        self._stats.set(Stats.newskills, value)

    @property
    def hitpoints(self):
        '''
        the characters current hit points
        '''
        return self._stats.get(Stats.hitpoints) / 256.0

    @hitpoints.setter
    def hitpoints(self, value):
        '''
        set the characters current hit points
        '''
        self._stats.set(Stats.hitpoints, value * 256)

    @property
    def maxhp(self):
        '''
        the characters maximum hitpoints
        '''
        return self._stats.get(Stats.maxhp) / 256.0

    @maxhp.setter
    def maxhp(self, value):
        '''
        set the characters maximum hitpoints
        '''
        self._stats.set(Stats.maxhp, value * 256)

    @property
    def mana(self):
        '''
        the characters current mana points
        '''
        return self._stats.get(Stats.mana) / 256.0

    @mana.setter
    def mana(self, value):
        '''
        set the characters current mana points
        '''
        self._stats.set(Stats.mana, value * 256)

    @property
    def maxmana(self):
        '''
        the characters maximum mana points
        '''
        return self._stats.get(Stats.maxmana) / 256.0

    @maxmana.setter
    def maxmana(self, value):
        '''
        set the characters maximum mana points
        '''
        self._stats.set(Stats.maxmana, value * 256)

    @property
    def stamina(self):
        '''
        the characters current stamina points
        '''
        return self._stats.get(Stats.stamina) / 256.0

    @stamina.setter
    def stamina(self, value):
        '''
        set the characters current stamina points
        '''
        self._stats.set(Stats.stamina, value * 256)

    @property
    def maxstamina(self):
        '''
        the characters maximum stamina points
        '''
        return self._stats.get(Stats.maxstamina) / 256.0

    @maxstamina.setter
    def maxstamina(self, value):
        '''
        set the characters maximum stamina points
        '''
        self._stats.set(Stats.maxstamina, value * 256)

    @property
    def experience(self):
        '''
        the characters current experience points
        '''
        return self._stats.get(Stats.experience)

    @experience.setter
    def experience(self, value):
        '''
        set the characters current experience points
        '''
        self._stats.set(Stats.experience, value)

    @property
    def gold(self):
        '''
        the characters current gold
        '''
        return self._stats.get(Stats.gold)

    @gold.setter
    def gold(self, value):
        '''
        set the characters current gold
        '''
        self._stats.set(Stats.gold, value)

    @property
    def goldbank(self):
        '''
        the characters current gold in the stash
        '''
        return self._stats.get(Stats.goldbank)

    @goldbank.setter
    def goldbank(self, value):
        '''
        set the characters current gold in the stash
        '''
        self._stats.set(Stats.goldbank, value)
