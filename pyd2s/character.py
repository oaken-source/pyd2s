
'''
this module provides a class that manages character data
'''

import re
from os.path import dirname, join, isfile

from pyd2s.basictypes import CharacterClass


STATS = [
    ('strength', 10),
    ('energy', 10),
    ('dexterity', 10),
    ('vitality', 10),
    ('statpts', 10),
    ('newskills', 8),
    ('hitpoints', 21),
    ('maxhp', 21),
    ('mana', 21),
    ('maxmana', 21),
    ('stamina', 21),
    ('maxstama', 21),
    ('level', 7),
    ('experience', 32),
    ('gold', 25),
    ('goldbank', 25),
]


class Character(object):
    '''
    save data referring to the character itself
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        self._strength = None
        self._energy = None
        self._dexterity = None
        self._vitality = None

        self._statpts = None
        self._newskills = None

        self._hitpoints = None
        self._maxhp = None
        self._mana = None
        self._maxmana = None
        self._stamina = None
        self._maxstamina = None

        self._level = None
        self._experience = None
        self._gold = None
        self._goldbank = None

        self._extract_stats()

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
        self._set_stat(self._level, value, 7)

    def _extract_stats(self):
        '''
        parse the stats section for positions of stat fields
        '''

        position = 767 * 8
        while True:
            statid = self._buffer.getbits(position, 9)
            if statid == 0x1FF:
                break
            setattr(self, '_' + STATS[statid][0], position + 9)
            position += 9 + STATS[statid][1]

    def _get_stat(self, position, length):
        '''
        produce a stat info field from a given position and length
        '''
        return 0 if position is None else self._buffer.getbits(position, length)

    def _set_stat(self, position, value, length):
        '''
        set a stat info field
        '''
        if position is not None:
            self._buffer.setbits(position, value, length)

    @property
    def strength(self):
        '''
        the characters strength
        '''
        return self._get_stat(self._strength, 10)

    @strength.setter
    def strength(self, value):
        '''
        set the characters strength
        '''
        self._set_stat(self._strength, value, 10)

    @property
    def energy(self):
        '''
        the characters energy
        '''
        return self._get_stat(self._energy, 10)

    @energy.setter
    def energy(self, value):
        '''
        set the characters energy
        '''
        self._set_stat(self._energy, value, 10)

    @property
    def dexterity(self):
        '''
        the characters dexterity
        '''
        return self._get_stat(self._dexterity, 10)

    @dexterity.setter
    def dexterity(self, value):
        '''
        set the characters dexterity
        '''
        self._set_stat(self._dexterity, value, 10)

    @property
    def vitality(self):
        '''
        the characters vitality
        '''
        return self._get_stat(self._vitality, 10)

    @vitality.setter
    def vitality(self, value):
        '''
        set the characters vitality
        '''
        self._set_stat(self._vitality, value, 10)

    @property
    def statpts(self):
        '''
        the characters unassigned stat points
        '''
        return self._get_stat(self._statpts, 10)

    @statpts.setter
    def statpts(self, value):
        '''
        set the characters unassigned stat points
        '''
        self._set_stat(self._statpts, value, 10)

    @property
    def newskills(self):
        '''
        the characters unassigned skill points
        '''
        return self._get_stat(self._newskills, 8)

    @newskills.setter
    def newskills(self, value):
        '''
        set the characters unassigned skill points
        '''
        self._set_stat(self._newskills, value, 8)

    @property
    def hitpoints(self):
        '''
        the characters current hit points
        '''
        return self._get_stat(self._hitpoints, 21) / 256.0

    @hitpoints.setter
    def hitpoints(self, value):
        '''
        set the characters current hit points
        '''
        self._set_stat(self._hitpoints, value * 256, 21)

    @property
    def maxhp(self):
        '''
        the characters maximum hitpoints
        '''
        return self._get_stat(self._maxhp, 21) / 256.0

    @maxhp.setter
    def maxhp(self, value):
        '''
        set the characters maximum hitpoints
        '''
        self._set_stat(self._maxhp, value * 256, 21)

    @property
    def mana(self):
        '''
        the characters current mana points
        '''
        return self._get_stat(self._mana, 21) / 256.0

    @mana.setter
    def mana(self, value):
        '''
        set the characters current mana points
        '''
        self._set_stat(self._mana, value * 256, 21)

    @property
    def maxmana(self):
        '''
        the characters maximum mana points
        '''
        return self._get_stat(self._maxmana, 21) / 256.0

    @maxmana.setter
    def maxmana(self, value):
        '''
        set the characters maximum mana points
        '''
        self._set_stat(self._maxmana, value * 256, 21)

    @property
    def stamina(self):
        '''
        the characters current stamina points
        '''
        return self._get_stat(self._stamina, 21) / 256.0

    @stamina.setter
    def stamina(self, value):
        '''
        set the characters current stamina points
        '''
        self._set_stat(self._stamina, value * 256, 21)

    @property
    def maxstamina(self):
        '''
        the characters maximum stamina points
        '''
        return self._get_stat(self._maxstamina, 21) / 256.0

    @maxstamina.setter
    def maxstamina(self, value):
        '''
        set the characters maximum stamina points
        '''
        self._set_stat(self._maxstamina, value * 256, 21)

    @property
    def experience(self):
        '''
        the characters current experience points
        '''
        return self._get_stat(self._experience, 32)

    @experience.setter
    def experience(self, value):
        '''
        set the characters current experience points
        '''
        self._set_stat(self._experience, value, 32)

    @property
    def gold(self):
        '''
        the characters current gold
        '''
        return self._get_stat(self._gold, 25)

    @gold.setter
    def gold(self, value):
        '''
        set the characters current gold
        '''
        self._set_stat(self._gold, value, 25)

    @property
    def goldbank(self):
        '''
        the characters current gold in the stash
        '''
        return self._get_stat(self._goldbank, 25)

    @goldbank.setter
    def goldbank(self, value):
        '''
        set the characters current gold in the stash
        '''
        self._set_stat(self._goldbank, value, 25)
