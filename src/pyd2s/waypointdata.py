
'''
this module provides classes to manage waypoint data of a d2s save
'''

import struct
from enum import Enum

from pyd2s.gamedata import GameData


class Waypoint(Enum):
    '''
    the waypoints available in the game
    '''
    ROGUE_ENCAMPMENT = 0
    COLD_PLAINS = 1
    STONY_FIELD = 2
    DARK_WOOD = 3
    BLACK_MARSH = 4
    OUTER_CLOISTER = 5
    JAIL_LEVEL_1 = 6
    INNER_CLOISTER = 7
    CATACOMBS_LEVEL_2 = 8
    LUT_GHOLEIN = 9
    SEWERS_LEVEL_2 = 10
    DRY_HILLS = 11
    HALLS_OF_THE_DEAD_LEVEL_2 = 12
    FAR_OASIS = 13
    LOST_CITY = 14
    PALACE_CELLAR_LEVEL_1 = 15
    ARCANE_SANCTUARY = 16
    CANYON_OF_THE_MAGI = 17
    KURAST_DOCKS = 18
    SPIDER_FOREST = 19
    GREAT_MARSH = 20
    FLAYER_JUNGLE = 21
    LOWER_KURAST = 22
    KURAST_BAZAAR = 23
    UPPER_KURAST = 24
    TRAVINCAL = 25
    DURANCE_OF_HATE_LEVEL_2 = 26
    PANDEMONIUM_FORTRESS = 27
    CITY_OF_THE_DAMNED = 28
    RIVER_OF_FLAMES = 29
    HARROGATH = 30
    FRIGID_HIGHLANDS = 31
    ARREAT_PLATEAU = 32
    CRYSTALLINE_PASSAGE = 33
    HALLS_OF_PAIN = 34
    GLACIAL_TRAIL = 35
    FROZEN_TUNDRA = 36
    THE_ANCIENTS_WAY = 37
    WORLDSTONE_KEEP_LEVEL_2 = 38

    @property
    def act(self):
        '''
        produce the act of the quest from the game data
        '''
        return self.value // 9 + 1

    def __str__(self):
        '''
        produce the name of the quest from the game data
        '''
        data = next(data for data in GameData.levels if int(data['Waypoint']) == self.value)
        return GameData.get_string(f'{data["LevelName"]}')


# pylint: disable=R0903
class WaypointData:
    '''
    save data related to waypoints
    '''

    class WaypointData:
        '''
        waypoint data for a single difficulty
        '''

        def __init__(self, buffer, offset):
            '''
            constructor - propagate buffer and offset
            '''
            self._buffer = buffer
            self._offset = offset

        @property
        def _value(self):
            '''
            produce the raw value of the waypoint data
            '''
            low, high = struct.unpack_from('<LB', self._buffer, 643 + self._offset)
            return (high << 32) | low

        @_value.setter
        def _value(self, value):
            '''
            set the new raw value of the waypoint data
            '''
            high = value >> 32
            low = value & 0xffffffff
            struct.pack_into('<LB', self._buffer, 643 + self._offset, low, high)

        def __getitem__(self, waypoint):
            '''
            True if the given waypoint is active, False otherwise
            '''
            if not isinstance(waypoint, Waypoint):
                waypoint = Waypoint(waypoint)

            if self._buffer.sparse:
                return waypoint == Waypoint.ROGUE_ENCAMPMENT

            return (self._value & (1 << waypoint.value)) != 0

        def __setitem__(self, waypoint, value):
            '''
            set the state of a given waypoint
            '''
            if self._buffer.sparse:
                raise ValueError('unable to set waypoint data on sparse save.')

            if not isinstance(waypoint, Waypoint):
                waypoint = Waypoint(waypoint)

            if value:
                self._value = self._value | (1 << waypoint.value)
            else:
                self._value = self._value & ~(1 << waypoint.value)

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        if self._header != 'WS':
            raise ValueError('invalid save: mismatched waypoint section header')

        self.normal = self.WaypointData(buffer, 0)
        self.nightmare = self.WaypointData(buffer, 0x18)
        self.hell = self.WaypointData(buffer, 0x30)

    @property
    def _header(self):
        '''
        produce the header of the section - should be 'WS'
        '''
        if self._buffer.sparse:
            return 'WS'
        return self._buffer[633:635].decode('ascii')
