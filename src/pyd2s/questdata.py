
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

            if self._buffer.sparse:
                return 0

            return struct.unpack_from('<H', self._buffer, 345 + self._offset + quest.offset)[0]

        def __setitem__(self, quest, value):
            if self._buffer.sparse:
                raise ValueError('unable to set quest data on sparse save.')

            if not isinstance(quest, Quest):
                quest = Quest(quest)

            struct.pack_into('<H', self._buffer, 345 + self._offset + quest.offset, value)


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
        if self._buffer.sparse:
            return 'Woo!'
        return self._buffer[335:339].decode('ascii')
