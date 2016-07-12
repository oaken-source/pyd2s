
'''
This module provides classes to manage D2 save games.
'''

import struct

from pyd2s.savebuffer import SaveBuffer
from pyd2s.basictypes import CharacterClass, Difficulty, Act


class D2SaveFile(object):
    '''
    a .d2s file containing diablo 2 save game data
    '''

    def __init__(self, path):
        '''
        constructor - mmap file data and do sanity checks
        '''
        self._path = path
        self._buffer = SaveBuffer(path)

        if self.magic != 0xaa55aa55:
            raise ValueError('invalid save: mismatched magic number')
        if self.version != 0x60:
            raise NotImplementedError('invalid save: unsupported version %#x' % self.version)

        self.character = Character(self._buffer)
        self.mercenary = Mercenary(self._buffer)
        self.questdata = QuestData(self._buffer)
        self.waypoints = WaypointData(self._buffer)

    @property
    def magic(self):
        '''
        the magic number of d2s files - should be 0xaa55aa55
        '''
        return struct.unpack('<L', self._buffer[0:4])[0]

    @property
    def version(self):
        '''
        the version of the file - supported values are 0x60 for >=1.10
        '''
        return struct.unpack('<L', self._buffer[4:8])[0]


class Character(object):
    '''
    save data referring to the character itself
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

    @property
    def active_arms(self):
        '''
        the number of the currently active weapon set of the character
        '''
        return struct.unpack('<L', self._buffer[16:20])[0]

    @property
    def name(self):
        '''
        the name of the character
        '''
        return self._buffer[20:36].decode('ascii').rstrip('\0')

    @property
    def is_ladder(self):
        '''
        True if the character is in the ladder, False otherwise
        '''
        return (self._buffer[36] & (1 << 6)) != 0

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

    @property
    def is_hardcore(self):
        '''
        True if the character is a hardcore character, False otherwise
        '''
        return (self._buffer[36] & (1 << 2)) != 0

    @property
    def progression(self):
        '''
        an integer representing the characters progress in the game and its title
        '''
        return self._buffer[37]

    @property
    def character_class(self):
        '''
        the class of the character
        '''
        return CharacterClass(self._buffer[40])

    @property
    def level(self):
        '''
        the current level of the character
        '''
        return self._buffer[43]

    @property
    def skill_hotkeys(self):
        '''
        the list of assigned skills to the 16 hot keys
        '''
        return struct.unpack('<16L', self._buffer[56:120])

    @property
    def skill_leftclick(self):
        '''
        the skill assigned to left click of weapon set 1
        '''
        return struct.unpack('<L', self._buffer[120:124])[0]

    @property
    def skill_rightclick(self):
        '''
        the skill assigned to right click of weapon set 1
        '''
        return struct.unpack('<L', self._buffer[124:128])[0]

    @property
    def skill_alt_leftclick(self):
        '''
        the skill assigned to left click of weapon set 2
        '''
        return struct.unpack('<L', self._buffer[128:132])[0]

    @property
    def skill_alt_rightclick(self):
        '''
        the skill assigned to right click of weapon set 2
        '''
        return struct.unpack('<L', self._buffer[132:136])[0]

    @property
    def current_difficulty(self):
        '''
        the last played difficulty
        '''
        if self._buffer[168]:
            return Difficulty.Normal
        if self._buffer[169]:
            return Difficulty.Nightmare
        return Difficulty.Hell

    @property
    def current_act(self):
        '''
        the last played act
        '''
        return Act(self._buffer[168 + self.current_difficulty.value] & 0x3)

    @property
    def map_seed(self):
        '''
        the map generation seed
        '''
        return struct.unpack('<L', self._buffer[171:175])[0]


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
    def type(self):
        '''
        the type of the active mercenary - encodes act and capabilities
        '''
        return struct.unpack('<H', self._buffer[185:187])[0]

    @property
    def experience(self):
        '''
        the experience points of the active mercenary
        '''
        return struct.unpack('<L', self._buffer[187:191])[0]


class QuestData(object):
    '''
    save data referring to quest completion
    '''

    class QuestData(object):
        '''
        the quest completion data of a specific difficulty level
        '''

        def __init__(self, buffer, offset):
            '''
            constructor - propagate buffer and offset
            '''
            self._buffer = buffer
            self._offset = offset

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        if self._header != 'Woo!':
            raise ValueError('invalid save file')

        self.normal = self.QuestData(buffer, 0)
        self.nightmare = self.QuestData(buffer, 0x60)
        self.hell = self.QuestData(buffer, 0xc0)

    @property
    def _header(self):
        '''
        the header of the quest data section - should be 'Woo!'
        '''
        return self._buffer[335:339].decode('ascii')


class WaypointData(object):
    '''
    save data referring to waypoints
    '''

    class WaypointData(object):
        '''
        the waypoint data of a specific difficulty level
        '''

        def __init__(self, buffer, offset):
            '''
            constructor - propagate buffer and offset
            '''
            self._buffer = buffer
            self._offset = offset

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        if self._header != 'WS':
            raise ValueError('invalid save file')

        self.normal = self.WaypointData(buffer, 0)
        self.nightmare = self.WaypointData(buffer, 0x18)
        self.hell = self.WaypointData(buffer, 0x30)

    @property
    def _header(self):
        '''
        the header of the waypoint data section - should be 'WS'
        '''
        return self._buffer[633:635].decode('ascii')
