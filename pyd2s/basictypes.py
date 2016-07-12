
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


class Waypoint(Enum):
    '''
    the waypoints available in the game
    '''
    RogueEncampment = 0x0000000001
    ColdPlains = 0x0000000002
    StonyField = 0x0000000004
    DarkWood = 0x0000000008
    BlackMarsh = 0x0000000010
    OuterCloister = 0x0000000020
    JailLlevel1 = 0x0000000040
    InnerCloister = 0x0000000080
    CatacombsLevel2 = 0x0000000100
    LutGholein = 0x0000000200
    SewersLevel2 = 0x0000000400
    DryHills = 0x0000000800
    HallsOfTheDeadLevel2 = 0x0000001000
    FarOasis = 0x0000002000
    LostCity = 0x0000004000
    PalaceCellarLevel1 = 0x0000008000
    ArcaneSanctuary = 0x0000010000
    CanyonOfTheMagi = 0x0000020000
    KurastDocks = 0x0000040000
    SpiderForest = 0x0000080000
    GreatMarsh = 0x0000100000
    FlayerJungle = 0x0000200000
    LowerKurast = 0x0000400000
    KurastBazaar = 0x0000800000
    UpperKurast = 0x0001000000
    Travincal = 0x0002000000
    DuranceOfHateLevel2 = 0x0004000000
    PandemoniumFortress = 0x0008000000
    CityOfTheDamned = 0x0010000000
    RiverOfFlames = 0x0020000000
    Harrogath = 0x0040000000
    FrigidHighlands = 0x0080000000
    ArreatPlateau = 0x0100000000
    CrystallinePassage = 0x0200000000
    HallsOfPain = 0x0400000000
    GlacialTrail = 0x0800000000
    FrozenTundra = 0x1000000000
    TheAncientsWay = 0x2000000000
    WorldstoneKeepLevel2 = 0x4000000000
