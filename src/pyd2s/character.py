
'''
this module provides a class that manages character data
'''

import re
from os.path import dirname, join, isfile

from pyd2s.basictypes import CharacterClass, CharacterStat


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

            self._positions = {stat: None for stat in CharacterStat}
            self._end = 0

            position = 767 * 8
            while True:
                statid = self._buffer.getbits(position, 9)
                if statid == 0x1FF:
                    break
                stat = CharacterStat(statid)
                self._positions[stat] = position + 9
                position += 9 + stat.bits
            self._stats_end = position

        def get(self, statid):
            '''
            get the stat by id
            '''
            position = self._positions[statid]
            if position is None:
                return 0
            return self._buffer.getbits(position, statid.bits)

        def set(self, statid, value):
            '''
            set the stat by id to value
            '''
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


    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        self.stats = self.StatData(self._buffer)

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

    @is_expansion.setter
    def is_expansion(self, value):
        '''
        set wether the character is in the expansion
        '''
        if not value and self.character_class in (CharacterClass.ASSASSIN, CharacterClass.DRUID):
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
        if value in (CharacterClass.ASSASSIN, CharacterClass.DRUID) and not self.is_expansion:
            raise ValueError('assassins and druids need expansion flag set')
        self._buffer[40] = value.value
