
'''
This module provides character stat metadata
'''

from enum import Enum


class Stats(Enum):
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


STATBITS = {
    Stats.strength: 10,
    Stats.energy: 10,
    Stats.dexterity: 10,
    Stats.vitality: 10,
    Stats.statpts: 10,
    Stats.newskills: 8,
    Stats.hitpoints: 21,
    Stats.maxhp: 21,
    Stats.mana: 21,
    Stats.maxmana: 21,
    Stats.stamina: 21,
    Stats.maxstamina: 21,
    Stats.level: 7,
    Stats.experience: 32,
    Stats.gold: 25,
    Stats.goldbank: 25,
}

class StatData(object):
    '''
    this class provides access to a characters stat data
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer and parse stats section
        '''
        self._buffer = buffer

        self._positions = {stat: None for stat in Stats}
        self._end = 0

        position = 767 * 8
        while True:
            statid = self._buffer.getbits(position, 9)
            if statid == 0x1FF:
                break
            stat = Stats(statid)
            self._positions[stat] = position + 9
            position += 9 + STATBITS[stat]
        self._stats_end = position

    def get(self, statid):
        '''
        get the stat by id
        '''
        position = self._positions[statid]
        if position is None:
            return 0
        return self._buffer.getbits(position, STATBITS[statid])

    def set(self, statid, value):
        '''
        set the stat by id to value
        '''
        if value.bit_length() > STATBITS[statid]:
            raise ValueError('value too large for stat %s' % statid.name)
        position = self._positions[statid]
        if position is None:
            self._positions[statid] = self._end
            self._buffer.addbits(self._end, 9 + STATBITS[statid], self._end + 9)
            self._buffer.setbits(self._end, statid.value, 9)
            self._buffer.setbits(self._end + 9, value, STATBITS[statid])
            self._end += 9 + STATBITS[statid]
        else:
            self._buffer.setbits(position, value, STATBITS[statid])

