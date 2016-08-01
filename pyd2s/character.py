
'''
this module provides a class that manages character data
'''

import re
from enum import Enum
from os.path import dirname, join, isfile

from pyd2s.basictypes import CharacterClass


class StatID(Enum):
    '''
    the stat ids known
    '''
    strength = 0x00
    energy = 0x01
    dexterity = 0x02
    vitality = 0x03
    statpts = 0x04
    newskills = 0x05
    hitpoints = 0x06
    maxhp = 0x07
    mana = 0x08
    maxmana = 0x09
    stamina = 0x0a
    maxstamina = 0x0b
    level = 0x0c
    experience = 0x0d
    gold = 0x0e
    goldbank = 0x0f


STATS = {
    StatID.strength: ('strength', 10),
    StatID.energy: ('energy', 10),
    StatID.dexterity: ('dexterity', 10),
    StatID.vitality: ('vitality', 10),
    StatID.statpts: ('statpts', 10),
    StatID.newskills: ('newskills', 8),
    StatID.hitpoints: ('hitpoints', 21),
    StatID.maxhp: ('maxhp', 21),
    StatID.mana: ('mana', 21),
    StatID.maxmana: ('maxmana', 21),
    StatID.stamina: ('stamina', 21),
    StatID.maxstamina: ('maxstamina', 21),
    StatID.level: ('level', 7),
    StatID.experience: ('experience', 32),
    StatID.gold: ('gold', 25),
    StatID.goldbank: ('goldbank', 25),
}


class Character(object):
    '''
    save data referring to the character itself
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        for statid in StatID:
            setattr(self, '_' + STATS[statid][0], None)

        self._stats_end = 0
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
        self._set_stat(StatID.level, value)

    def _extract_stats(self):
        '''
        parse the stats section for positions of stat fields
        '''
        position = 767 * 8
        while True:
            statid = self._buffer.getbits(position, 9)
            if statid == 0x1FF:
                break
            stat = StatID(statid)
            setattr(self, '_' + STATS[stat][0], position + 9)
            position += 9 + STATS[stat][1]
        self._stats_end = position

    def _get_stat(self, statid):
        '''
        get the stat by name
        '''
        stat = STATS[statid]
        position = getattr(self, '_' + stat[0])
        if position is None:
            return 0
        return self._buffer.getbits(position, stat[1])

    def _set_stat(self, statid, value):
        '''
        set the stat by name to value
        '''
        stat = STATS[statid]
        if value.bit_length() > stat[1]:
            raise ValueError('value too large for stat %s' % statid.name)
        position = getattr(self, '_' + stat[0])
        if position is None:
            setattr(self, '_' + stat[0], self._stats_end)
            self._buffer.addbits(self._stats_end, 9 + stat[1], self._stats_end + 9)
            self._buffer.setbits(self._stats_end, statid.value, 9)
            self._buffer.setbits(self._stats_end + 9, value, stat[1])
            self._stats_end += 9 + stat[1]
        else:
            self._buffer.setbits(position, value, stat[1])

    @property
    def strength(self):
        '''
        the characters strength
        '''
        return self._get_stat(StatID.strength)

    @strength.setter
    def strength(self, value):
        '''
        set the characters strength
        '''
        self._set_stat(StatID.strength, value)

    @property
    def energy(self):
        '''
        the characters energy
        '''
        return self._get_stat(StatID.energy)

    @energy.setter
    def energy(self, value):
        '''
        set the characters energy
        '''
        self._set_stat(StatID.energy, value)

    @property
    def dexterity(self):
        '''
        the characters dexterity
        '''
        return self._get_stat(StatID.dexterity)

    @dexterity.setter
    def dexterity(self, value):
        '''
        set the characters dexterity
        '''
        self._set_stat(StatID.dexterity, value)

    @property
    def vitality(self):
        '''
        the characters vitality
        '''
        return self._get_stat(StatID.vitality)

    @vitality.setter
    def vitality(self, value):
        '''
        set the characters vitality
        '''
        self._set_stat(StatID.vitality, value)

    @property
    def statpts(self):
        '''
        the characters unassigned stat points
        '''
        return self._get_stat(StatID.statpts)

    @statpts.setter
    def statpts(self, value):
        '''
        set the characters unassigned stat points
        '''
        self._set_stat(StatID.statpts, value)

    @property
    def newskills(self):
        '''
        the characters unassigned skill points
        '''
        return self._get_stat(StatID.newskills)

    @newskills.setter
    def newskills(self, value):
        '''
        set the characters unassigned skill points
        '''
        self._set_stat(StatID.newskills, value)

    @property
    def hitpoints(self):
        '''
        the characters current hit points
        '''
        return self._get_stat(StatID.hitpoints) / 256.0

    @hitpoints.setter
    def hitpoints(self, value):
        '''
        set the characters current hit points
        '''
        self._set_stat(StatID.hitpoints, value * 256)

    @property
    def maxhp(self):
        '''
        the characters maximum hitpoints
        '''
        return self._get_stat(StatID.maxhp) / 256.0

    @maxhp.setter
    def maxhp(self, value):
        '''
        set the characters maximum hitpoints
        '''
        self._set_stat(StatID.maxhp, value * 256)

    @property
    def mana(self):
        '''
        the characters current mana points
        '''
        return self._get_stat(StatID.mana) / 256.0

    @mana.setter
    def mana(self, value):
        '''
        set the characters current mana points
        '''
        self._set_stat(StatID.mana, value * 256)

    @property
    def maxmana(self):
        '''
        the characters maximum mana points
        '''
        return self._get_stat(StatID.maxmana) / 256.0

    @maxmana.setter
    def maxmana(self, value):
        '''
        set the characters maximum mana points
        '''
        self._set_stat(StatID.maxmana, value * 256)

    @property
    def stamina(self):
        '''
        the characters current stamina points
        '''
        return self._get_stat(StatID.stamina) / 256.0

    @stamina.setter
    def stamina(self, value):
        '''
        set the characters current stamina points
        '''
        self._set_stat(StatID.stamina, value * 256)

    @property
    def maxstamina(self):
        '''
        the characters maximum stamina points
        '''
        return self._get_stat(StatID.maxstamina) / 256.0

    @maxstamina.setter
    def maxstamina(self, value):
        '''
        set the characters maximum stamina points
        '''
        self._set_stat(StatID.maxstamina, value * 256)

    @property
    def experience(self):
        '''
        the characters current experience points
        '''
        return self._get_stat(StatID.experience)

    @experience.setter
    def experience(self, value):
        '''
        set the characters current experience points
        '''
        self._set_stat(StatID.experience, value)

    @property
    def gold(self):
        '''
        the characters current gold
        '''
        return self._get_stat(StatID.gold)

    @gold.setter
    def gold(self, value):
        '''
        set the characters current gold
        '''
        self._set_stat(StatID.gold, value)

    @property
    def goldbank(self):
        '''
        the characters current gold in the stash
        '''
        return self._get_stat(StatID.goldbank)

    @goldbank.setter
    def goldbank(self, value):
        '''
        set the characters current gold in the stash
        '''
        self._set_stat(StatID.goldbank, value)
