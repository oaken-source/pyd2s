
'''
this module provides a class to manage mercenary data
'''

import struct

from pyd2s.basictypes import MercenaryType


class Mercenary:
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
        return struct.unpack_from('<H', self._buffer, 177)[0] != 0

    @is_dead.setter
    def is_head(self, value):
        '''
        set whether the mercenary is dead
        '''
        struct.pack_into('<H', self._buffer, 177, bool(value))

    @property
    def control_seed(self):
        '''
        the mercenary control seed
        '''
        return struct.unpack_from('<L', self._buffer, 179)[0]

    @control_seed.setter
    def control_seed(self, value):
        '''
        set the mercenary control seed
        '''
        struct.pack_into('<L', self._buffer, 179, value)

    @property
    def name_id(self):
        '''
        the id into the language dependent mercenary name table
        '''
        return struct.unpack_from('<H', self._buffer, 183)[0]

    @name_id.setter
    def name_id(self, value):
        '''
        set the name id of the mercenary
        '''
        struct.pack_into('<H', self._buffer, 183, value)

    @property
    def type(self):
        '''
        the type of the active mercenary - encodes act and capabilities
        '''
        return MercenaryType(struct.unpack_from('<H', self._buffer, 185)[0])

    @type.setter
    def type(self, value):
        '''
        set the type of the active mercenary
        '''
        if not isinstance(value, MercenaryType):
            value = MercenaryType(value)
        struct.pack_into('<H', self._buffer, 185, value.value)

    @property
    def experience(self):
        '''
        the experience points of the active mercenary
        '''
        return struct.unpack_from('<L', self._buffer, 187)[0]

    @experience.setter
    def experience(self, value):
        '''
        set the experience of the mercenary
        '''
        struct.pack_into('<H', self._buffer, 187, value)
