
'''
this module provides a class that manages character data
'''

import re
import math
from os.path import dirname, join, isfile

from pyd2s.basictypes import CharacterClass, CharacterStat, SkillTree
from pyd2s.gamedata import GameData


class Character:
    '''
    save data referring to the character itself
    '''

    class StatData:
        '''
        this class provides access to a characters stat data
        '''

        def __init__(self, buffer):
            '''
            constructor - propagate buffer and parse stats section
            '''
            self._buffer = buffer

            if self._header != 'gf':
                raise ValueError('invalid save: mismatched stat data section header')

            self._positions = {stat: None for stat in CharacterStat}
            self._end = 0
            self._stats_end = 0

            # if this is a sparse save file, we can stop looking for stat data
            if self._buffer.sparse:
                return

            position = 767 * 8
            while True:
                statid = self._buffer.getbits(position, 9)
                if statid == 0x1FF:
                    break
                stat = CharacterStat(statid)
                self._positions[stat] = position + 9
                position += 9 + stat.bits
            self._end = position

        @property
        def _header(self):
            '''
            produce the header of the section - should be 'gf'
            '''
            if self._buffer.sparse:
                return 'gf'
            return self._buffer[765:767].decode('ascii')

        @property
        def length(self):
            '''
            the length of the stat section in bytes
            '''
            return math.ceil((self._end + 9) / 8) - 765

        def __getitem__(self, statid):
            '''
            get the stat by id
            '''
            position = self._positions[statid]
            if position is None:
                return 0
            return self._buffer.getbits(position, statid.bits)

        def __setitem__(self, statid, value):
            '''
            set the stat by id to value
            '''
            if self._buffer.sparse:
                raise ValueError('unable to set stat data on sparse save.')

            if value.bit_length() > statid.bits:
                raise ValueError(f'value too large for stat {statid}')

            position = self._positions[statid]
            if position is None:
                self._positions[statid] = self._end
                self._buffer.addbits(self._end, 9 + statid.bits, self._end + 9)
                self._buffer.setbits(self._end, statid.value, 9)
                self._buffer.setbits(self._end + 9, value, statid.bits)
                self._end += 9 + statid.bits
            else:
                self._buffer.setbits(position, value, statid.bits)

            # when updating the level, also update in the character data
            if statid == CharacterStat.LEVEL:
                self._buffer[43] = value

    class SkillData:
        '''
        this class provides access to a characters stat data
        '''

        def __init__(self, buffer, offset):
            '''
            constructor - propagate buffer and parse stats section
            '''
            self._buffer = buffer
            self._offset = offset

            if self._header != 'if':
                raise ValueError('invalid save: mismatched stat data section header')

        @property
        def _header(self):
            '''
            produce the header of the section - should be 'if'
            '''
            if self._buffer.sparse:
                return 'if'
            return self._buffer[self._offset:self._offset + 2].decode('ascii')

        def __getitem__(self, skillid):
            '''
            get the skill by id
            '''
            if isinstance(skillid, SkillTree):
                skillid = skillid.value

            if self._buffer.sparse:
                return 0

            return self._buffer[self._offset + 2 + skillid]

        def __setitem__(self, skillid, value):
            '''
            set the skill by id to value
            '''
            if self._buffer.sparse:
                raise ValueError('unable to set skill data on sparse save.')

            if isinstance(skillid, SkillTree):
                skillid = skillid.value

            self._buffer[self._offset + 2 + skillid] = value

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        GameData.set_expansion(self.is_expansion)

        self.stats = self.StatData(self._buffer)
        self.skills = self.SkillData(self._buffer, 765 + self.stats.length)

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

        newpath = join(dirname(self._buffer.path), f"{value}.d2s")
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
        if value in (CharacterClass.ASSASSIN, CharacterClass.DRUID) and not self.is_expansion:
            raise ValueError('assassins and druids need expansion flag set')
        self._buffer[40] = value.value
