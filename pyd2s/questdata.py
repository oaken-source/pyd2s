
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

    def _getoffset(self, difficulty):
        if difficulty == 0:
            offset = 345
        elif difficulty == 1:
            offset = 441
        elif difficulty == 2:
            offset = 537
        else:
            offset = 0
        return offset

    def get_act1_resetstatus(self, difficulty):
        '''
        Get Reset status end flag
        '''
        return (self._buffer[self._getoffset(difficulty) + 82] & 0x03) == 0x01

    def set_act1_resetstatus(self, difficulty, value):
        '''
        Set Reset status end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 82] &= ~0x03
            self._buffer[self._getoffset(difficulty) + 82] |=  0x01
        else:
            self._buffer[self._getoffset(difficulty) + 82] &= ~0x03
            self._buffer[self._getoffset(difficulty) + 82] |=  0x02

    def get_act1_forge(self, difficulty):
        '''
        Get Forge end flag
        '''
        return (self._buffer[self._getoffset(difficulty) + 6] & 0x03) == 0x01

    def set_act1_forge(self, difficulty, value):
        '''
        Set Forge end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 6] &= ~0x03
            self._buffer[self._getoffset(difficulty) + 6] |=  0x01
        else:
            self._buffer[self._getoffset(difficulty) + 6] &= ~0x03
            self._buffer[self._getoffset(difficulty) + 6] |=  0x02

    def get_act1_cowlevel(self, difficulty):
        '''
        Get Cow Level end flag
        '''
        return (self._buffer[self._getoffset(difficulty) + 9] & 0x04) != 0

    def set_act1_cowlevel(self, difficulty, value):
        '''
        Set Cow Level end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 9] |=  0x04
        else:
            self._buffer[self._getoffset(difficulty) + 9] &= ~0x04

    def get_act2_radament(self, difficulty):
        '''
        Get Radament quest end flag
        '''
        return self._buffer[self._getoffset(difficulty) + 18] == 0x1D and self._buffer[self._getoffset(difficulty) + 19] == 0x10

    def set_act2_radament(self, difficulty, value):
        '''
        Set Radament quest end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 18] = 0x1D
            self._buffer[self._getoffset(difficulty) + 19] = 0x10
        else:
            self._buffer[self._getoffset(difficulty) + 18] = 0x00
            self._buffer[self._getoffset(difficulty) + 19] = 0x00

    def get_act3_goldenbird(self, difficulty):
        '''
        Get Golden bird quest end flag
        '''
        return (self._buffer[self._getoffset(difficulty) + 40] == 0x01) and (self._buffer[self._getoffset(difficulty) + 41] == 0x10)

    def set_act3_goldenbird(self, difficulty, value):
        '''
        Set Golden bird quest end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 40] = 0x01
            self._buffer[self._getoffset(difficulty) + 41] = 0x10
        else:
            self._buffer[self._getoffset(difficulty) + 40] = 0x00
            self._buffer[self._getoffset(difficulty) + 41] = 0x00

    def get_act3_lamesen(self, difficulty):
        '''
        Get Lam Esen quest end flag
        '''
        return self._buffer[self._getoffset(difficulty) + 42] == 0x0D and self._buffer[self._getoffset(difficulty) + 43] == 0x10

    def set_act3_lamesen(self, difficulty, value):
        '''
        Set Lam Esen quest end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 42] = 0x0D
            self._buffer[self._getoffset(difficulty) + 43] = 0x10
        else:
            self._buffer[self._getoffset(difficulty) + 42] = 0x00
            self._buffer[self._getoffset(difficulty) + 43] = 0x00

    def get_act5_socket(self, difficulty):
        '''
        Get Socket end flag
        '''
        return (self._buffer[self._getoffset(difficulty) + 70] & 0x03) == 0x01

    def set_act5_socket(self, difficulty, value):
        '''
        Set Socket end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 70] &= ~0x03
            self._buffer[self._getoffset(difficulty) + 70] |=  0x01
        else:
            self._buffer[self._getoffset(difficulty) + 70] &= ~0x03
            self._buffer[self._getoffset(difficulty) + 70] |=  0x02

    def get_act5_runesset(self, difficulty):
        '''
        Get Giving runes set end flag
        '''
        return (self._buffer[self._getoffset(difficulty) + 70] & 0x20) != 0

    def set_act5_runesset(self, difficulty, value):
        '''
        Set Giving runes set end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 70] |=  0x20
        else:
            self._buffer[self._getoffset(difficulty) + 70] &= ~0x20

    def get_act5_scrollofregist(self, difficulty):
        '''
        Get Giving scroll of regist end flag
        '''
        return (self._buffer[self._getoffset(difficulty) + 74] & 0x80) != 0

    def set_act5_scrollofregist(self, difficulty, value):
        '''
        Set Giving scroll of regist end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 74] |=  0x80
        else:
            self._buffer[self._getoffset(difficulty) + 74] &= ~0x80

    def get_act5_personalize(self, difficulty):
        '''
        Get Socket end flag
        '''
        return (self._buffer[self._getoffset(difficulty) + 76] & 0x03) == 0x01

    def set_act5_personalize(self, difficulty, value):
        '''
        Set Socket end flag
        '''
        if value:
            self._buffer[self._getoffset(difficulty) + 76] &= ~0x03
            self._buffer[self._getoffset(difficulty) + 76] |=  0x01
        else:
            self._buffer[self._getoffset(difficulty) + 76] &= ~0x03
            self._buffer[self._getoffset(difficulty) + 76] |=  0x02

