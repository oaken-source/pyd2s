
'''
this module provides classes to manage waypoint data of a d2s save
'''

import struct

from pyd2s.basictypes import Waypoint


class WaypointData(object):
    '''
    save data related to waypoints
    '''

    class WaypointData(object):
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
            if len(self._buffer) <= 335:
                return Waypoint.RogueEncampment.value

            low, high = struct.unpack('<LB', self._buffer[643 + self._offset:648 + self._offset])
            return (high << 32) | low

        def __getitem__(self, waypoint):
            '''
            True if the given waypoint is active, False otherwise
            '''
            return (self._value & (1 << waypoint)) != 0

        def __iter__(self):
            '''
            produce a dict of all waypoints and their current status
            '''
            return {waypoint: self[waypoint] for waypoint in Waypoint}.__iter__()


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
        return self._buffer[633:635].decode('ascii')
