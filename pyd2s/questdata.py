
'''
this module provides classes to manage quest completion data of a d2s save
'''

import struct


class QuestData(object):
    '''
    save data related to quest completion
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        if self._header != 'WS':
            raise ValueError('invalid save: mismatched waypoint section header')

    @property
    def _header(self):
        '''
        produce the header of the section - should be 'WS'
        '''
        return self._buffer[633:635].decode('ascii')
