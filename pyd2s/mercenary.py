
'''
this module provides a class to manage mercenary data
'''

import struct

from pyd2s.basictypes import MercenaryTypes


class Mercenary(object):
    '''
    save data referring to the characters mercenary
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

    @property
    def is_dead(self):
        '''
        True if the mercenary is currently dead, False otherwise
        '''
        return struct.unpack('<H', self._buffer[177:179])[0] != 0

    @property
    def control_seed(self):
        '''
        the mercenary control seed
        '''
        return struct.unpack('<L', self._buffer[179:183])[0]

    @property
    def name_id(self):
        '''
        the id into the language dependent mercenary name table
        '''
        return struct.unpack('<H', self._buffer[183:185])[0]

    @property
    def type_id(self):
        '''
        the type_id of the active mercenary - encodes act and capabilities
        '''
        return struct.unpack('<H', self._buffer[185:187])[0]

    @property
    def type(self):
        '''
        the type of the mercenary
        '''
        return MercenaryTypes(self.type_id)

    @property
    def experience(self):
        '''
        the experience points of the active mercenary
        '''
        return struct.unpack('<L', self._buffer[187:191])[0]
