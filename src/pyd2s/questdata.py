
'''
this module provides classes to manage quest completion data of a d2s save
'''

import struct
from enum import Enum

from pyd2s.gamedata import GameData


class Quest(Enum):
    '''
    the quests available in the game
    '''
    DEN_OF_EVIL = 0
    SISTERS_BURIAL_GROUNDS = 1
    TOOLS_OF_THE_TRADE = 2
    THE_SEARCH_FOR_CAIN = 3
    THE_FORGOTTEN_TOWER = 4
    SISTERS_TO_THE_SLAUGHTER = 5
    RADAMENTS_LAIR = 6
    THE_HORADRIC_STAFF = 7
    TAINTED_SUN = 8
    ARCANE_SANCTUARY = 9
    THE_SUMMONER = 10
    THE_SEVEN_TOMBS = 11
    LAM_ESENS_TOME = 12
    KHALIMS_WILL = 13
    BLADE_OF_THE_OLD_RELIGION = 14
    THE_GOLDEN_BIRD = 15
    THE_BLACKENED_TEMPLE = 16
    THE_GUARDIAN = 17
    THE_FALLEN_ANGEL = 18
    TERRORS_END = 19
    HELLS_FORGE = 20
    SIEGE_OF_HARROGATH = 24
    RESCUE_ON_MOUNT_ARREAT = 25
    PRISON_OF_ICE = 26
    BETRAYAL_OF_HARROGATH = 27
    RITE_OF_PASSAGE = 28
    EVE_OF_DESTRUCTION = 29

    @property
    def offset(self):
        '''
        the offset of this quest into the quest data structure
        '''
        res = 2 + self.value * 2 + self.value // 6 * 4
        if self.act == 5:
            # adjust for 3 quest gap in Act 4
            res += 4
        return res

    @property
    def act(self):
        '''
        produce the act of the quest from the game data
        '''
        return self.value // 6 + 1

    @property
    def quest_num(self):
        '''
        produce the quest number inside the act
        '''
        return self.value % 6 + 1

    def __str__(self):
        '''
        produce the name of the quest from the game data
        '''
        return GameData.get_string(f'qstsa{self.act}q{self.quest_num}')


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

            if len(self._buffer) <= 335:
                return 0

            return struct.unpack_from('<H', self._buffer, 345 + self._offset + quest.offset)[0]

        def __setitem__(self, quest, value):
            if len(self._buffer) <= 335:
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
        if len(self._buffer) <= 335:
            return 'Woo!'
        return self._buffer[335:339].decode('ascii')
