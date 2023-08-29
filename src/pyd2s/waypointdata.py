
'''
this module provides classes to manage waypoint data of a d2s save
'''

import struct

from pyd2s.basictypes import Waypoint


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
