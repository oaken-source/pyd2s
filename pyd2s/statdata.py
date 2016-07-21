
'''
this module provides access to the stat data of a d2s file
'''

import struct
import bitstruct


class BitFactory(object):
    '''
    produce a bit stream from the stat data
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer
        self._start = 767
        self._byte = 0
        self._bit = 0

    def next(self, count):
        '''
        produce an integer of the next count bits and advance the pointer
        '''
        out = 0
        for i in range(count):
            out |= ((self._buffer[self._start + self._byte] & (1 << self._bit)) != 0) << i
            self._bit, self._byte = (self._bit + 1) % 8, self._byte + (self._bit == 7)
        return out


class StatData(object):
    '''
    parse and provide stat data
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer and parse stat data
        '''
        self._buffer = buffer

        if self._header != 'gf':
            raise ValueError('invalid save: mismatched stats section header')

        self.strength = 0
        self.energy = 0
        self.dexterity = 0
        self.vitality = 0

        self.statpts = 0
        self.newskills = 0

        self.hitpoints = 0
        self.maxhp = 0
        self.mana = 0
        self.maxmana = 0
        self.stamina = 0
        self.maxstamina = 0

        self.level = 0
        self.experience = 0
        self.gold = 0
        self.goldbank = 0

        self._extract_stats()

    def _extract_stats(self):
        '''
        produce the actual stat data
        '''
        factory = BitFactory(self._buffer)

        while True:
            statid = factory.next(9)
            if statid == 0:
                self.strength = factory.next(10)
            elif statid == 1:
                self.energy = factory.next(10)
            elif statid == 2:
                self.dexterity = factory.next(10)
            elif statid == 3:
                self.vitality = factory.next(10)
            elif statid == 4:
                self.statpts = factory.next(10)
            elif statid == 5:
                self.newskills = factory.next(8)
            elif statid == 6:
                self.hitpoints = factory.next(21) / 256.0
            elif statid == 7:
                self.maxhp = factory.next(21) / 256.0
            elif statid == 8:
                self.mana = factory.next(21) / 256.0
            elif statid == 9:
                self.maxmana = factory.next(21) / 256.0
            elif statid == 10:
                self.stamina = factory.next(21) / 256.0
            elif statid == 11:
                self.maxstamina = factory.next(21) / 256.0
            elif statid == 12:
                self.level = factory.next(7)
            elif statid == 13:
                self.experience = factory.next(32)
            elif statid == 14:
                self.gold = factory.next(25)
            elif statid == 15:
                self.goldbank = factory.next(25)
            else:
                break

        print(self.__dict__)

    @property
    def _header(self):
        '''
        produce the header of the section - should be 'gf'
        '''
        return self._buffer[765:767].decode('ascii')

