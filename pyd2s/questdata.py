
'''
this module provides classes to manage quest completion data of a d2s save
'''

import struct

from pyd2s.basictypes import Quest


# pylint: disable=R0903
class QuestData:
    '''
    save data related to quest completion
    '''

    class QuestData:
        '''
        quest data for a single difficulty
        '''

        def __init__(self, buffer, offset):
            '''
            constructor
            '''
            self._buffer = buffer
            self._offset = offset

        def __getitem__(self, quest):
            '''
            an integer representing the current quest progress
            '''
            if not isinstance(quest, Quest):
                quest = Quest(quest)

            start = 345 + self._offset + quest.offset
            return struct.unpack('<H', self._buffer[start:start + 2])[0]

        def __setitem__(self, quest, value):
            if not isinstance(quest, Quest):
                quest = Quest(quest)

            start = 345 + self._offset + quest.offset
            struct.pack_into('<H', self._buffer, start, value)

        def __iter__(self):
            '''
            produce a dict of all waypoints and their current status
            '''
            return {quest: self[quest.value] for quest in Quest}.__iter__()


    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        if self._header != 'Woo!':
            raise ValueError('invalid save: mismatched questdata section header')

        self.normal = self.QuestData(buffer, 0)
        self.nightmare = self.QuestData(buffer, 0x60)
        self.hell = self.QuestData(buffer, 0xC0)

    @property
    def _header(self):
        '''
        produce the header of the section - should be 'Woo!'
        '''
        return self._buffer[335:339].decode('ascii')
