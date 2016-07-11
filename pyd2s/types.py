
'''
this module contains some basic enumerated types
'''

from enum import Enum


class CharacterClass(Enum):
    '''
    the character classes available in the game
    '''
    Amazon = 0x00
    Sorceress = 0x01
    Necromancer = 0x02
    Paladin = 0x03
    Barbarian = 0x04
    Druid = 0x05
    Assassin = 0x06

    @property
    def gender(self):
        '''
        produce the gender of characters of this class
        '''
        return Gender(self.value in [0x00, 0x01, 0x06])


class Gender(Enum):
    '''
    the gender of a character
    '''
    Male = 0
    Female = 1


class Difficulty(Enum):
    '''
    the difficulty levels available in the game
    '''
    Normal = 0x00
    Nightmare = 0x01
    Hell = 0x02


class Act(Enum):
    '''
    the acts available in the game
    '''
    Act1 = 0x00
    Act2 = 0x01
    Act3 = 0x02
    Act4 = 0x03
    Act5 = 0x04


