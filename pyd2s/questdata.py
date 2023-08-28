
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
            offset_of = {
                Quest.DenOfEvil : 2,
                Quest.SistersBurialGrounds : 4,
                Quest.ToolsOfTheTrade : 6,
                Quest.TheSearchForCain : 8,
                Quest.TheForgottenTower : 10,
                Quest.SistersToTheSlaughter : 12,
                Quest.RadamentsLair : 18,
                Quest.TheHoradricStaff : 20,
                Quest.TaintedSun : 22,
                Quest.ArcaneSanctuary : 24,
                Quest.TheSummoner : 26,
                Quest.TheSevenTombs : 28,
                Quest.LamEsensTome : 34,
                Quest.KhalimsWill : 36,
                Quest.BladeOfTheOldReligion : 38,
                Quest.TheGoldenBird : 40,
                Quest.TheBlackenedTemple : 42,
                Quest.TheGuardian : 44,
                Quest.TheFallenAngel : 50,
                Quest.TerrorsEnd : 52,
                Quest.HellsForge : 54,
                Quest.SiegeOfHarrogath : 70,
                Quest.RescueOnMountArreat : 72,
                Quest.PrisonOfIce : 74,
                Quest.BetrayalOfHarrogath : 76,
                Quest.RiteOfPassage : 78,
                Quest.EveOfDestruction : 80,
            }

            if not isinstance(quest, Quest):
                quest = Quest(quest)

            return struct.unpack('<H', self._buffer[345 + self._offset + offset_of[quest]:345 + self._offset + offset_of[quest] + 2])[0]

        def __setitem__(self, quest, value):
            offset_of = {
                Quest.DenOfEvil : 2,
                Quest.SistersBurialGrounds : 4,
                Quest.ToolsOfTheTrade : 6,
                Quest.TheSearchForCain : 8,
                Quest.TheForgottenTower : 10,
                Quest.SistersToTheSlaughter : 12,
                Quest.RadamentsLair : 18,
                Quest.TheHoradricStaff : 20,
                Quest.TaintedSun : 22,
                Quest.ArcaneSanctuary : 24,
                Quest.TheSummoner : 26,
                Quest.TheSevenTombs : 28,
                Quest.LamEsensTome : 34,
                Quest.KhalimsWill : 36,
                Quest.BladeOfTheOldReligion : 38,
                Quest.TheGoldenBird : 40,
                Quest.TheBlackenedTemple : 42,
                Quest.TheGuardian : 44,
                Quest.TheFallenAngel : 50,
                Quest.TerrorsEnd : 52,
                Quest.HellsForge : 54,
                Quest.SiegeOfHarrogath : 70,
                Quest.RescueOnMountArreat : 72,
                Quest.PrisonOfIce : 74,
                Quest.BetrayalOfHarrogath : 76,
                Quest.RiteOfPassage : 78,
                Quest.EveOfDestruction : 80,
            }

            if not isinstance(quest, Quest):
                quest = Quest(quest)

            struct.pack_into('<H', self._buffer, 345 + self._offset + offset_of[quest], value)

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
