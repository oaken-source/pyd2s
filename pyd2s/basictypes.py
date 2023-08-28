
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


class CharacterStat(Enum):
    '''
    the character stat ids and bit widths
    '''
    strength = 0x00
    energy = 0x01
    dexterity = 0x02
    vitality = 0x03
    statpts = 0x04
    newskills = 0x05
    hitpoints = 0x06
    maxhp = 0x07
    mana = 0x08
    maxmana = 0x09
    stamina = 0x0a
    maxstamina = 0x0b
    level = 0x0c
    experience = 0x0d
    gold = 0x0e
    goldbank = 0x0f

    @property
    def bits(self):
        '''
        the bit width of the stat value
        '''
        return {
            CharacterStat.strength: 10,
            CharacterStat.energy: 10,
            CharacterStat.dexterity: 10,
            CharacterStat.vitality: 10,
            CharacterStat.statpts: 10,
            CharacterStat.newskills: 8,
            CharacterStat.hitpoints: 21,
            CharacterStat.maxhp: 21,
            CharacterStat.mana: 21,
            CharacterStat.maxmana: 21,
            CharacterStat.stamina: 21,
            CharacterStat.maxstamina: 21,
            CharacterStat.level: 7,
            CharacterStat.experience: 32,
            CharacterStat.gold: 25,
            CharacterStat.goldbank: 25,
        }[self]

    def __str__(self):
        '''
        a string representation of the stat
        '''
        return self.name



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

class Quest(Enum):
    '''
    the quests available in the game
    '''
    DenOfEvil = 0
    SistersBurialGrounds = 1
    ToolsOfTheTrade = 2
    TheSearchForCain = 3
    TheForgottenTower = 4
    SistersToTheSlaughter = 5
    RadamentsLair = 6
    TheHoradricStaff = 7
    TaintedSun = 8
    ArcaneSanctuary = 9
    TheSummoner = 10
    TheSevenTombs = 11
    LamEsensTome = 12
    KhalimsWill = 13
    BladeOfTheOldReligion = 14
    TheGoldenBird = 15
    TheBlackenedTemple = 16
    TheGuardian = 17
    TheFallenAngel = 18
    TerrorsEnd = 19
    HellsForge = 20
    SiegeOfHarrogath = 21
    RescueOnMountArreat = 22
    PrisonOfIce = 23
    BetrayalOfHarrogath = 24
    RiteOfPassage = 25
    EveOfDestruction = 26

class MercenaryTypes(Enum):
    '''
    the mercenary types available in the game
    '''
    RogueFireNormal = 0
    RogueColdNormal = 1
    RogueFireNightmare = 2
    RogueColdNightmare = 3
    RogueFireHell = 4
    RogueColdHell = 5
    DesertCombatNormal = 6
    DesertDefensiveNormal = 7
    DesertOffensiveNormal = 8
    DesertCombatNightmare = 9
    DesertDefensiveNightmare = 10
    DesertOffensiveNightmare = 11
    DesertCombatHell = 12
    DesertDefensiveHell = 13
    DesertOffensiveHell = 14
    SorcerorFireNormal = 15
    SorcerorColdNormal = 16
    SorcerorLightningNormal = 17
    SorcerorFireNightmare = 18
    SorcerorColdNightmare = 19
    SorcerorLightningNightmare = 20
    SorcerorFireHell = 21
    SorcerorColdHell = 22
    SorcerorLightningHell = 23
    BarbarianNormalA = 24
    BarbarianNormalB = 25
    BarbarianNightmareA = 26
    BarbarianNightmareB = 27
    BarbarianHellA = 28
    BarbarianHellB = 29

    def __str__(self):
        values = {
            0: "Rogue Scout - Fire Arrow (Normal)",
            1: "Rogue Scout - Cold Arrow (Normal)",
            2: "Rogue Scout - Fire Arrow (Nightmare)",
            3: "Rogue Scout - Cold Arrow (Nightmare)",
            4: "Rogue Scout - Fire Arrow (Hell)",
            5: "Rogue Scout - Cold Arrow (Hell)",
            6: "Desert Mercenary - Combat (Normal)",
            7: "Desert Mercenary - Defensive (Normal)",
            8: "Desert Mercenary - Offensive (Normal)",
            9: "Desert Mercenary - Combat (Nightmare)",
            10: "Desert Mercenary - Defensive (Nightmare)",
            11: "Desert Mercenary - Offensive (Nightmare)",
            12: "Desert Mercenary - Combat (Hell)",
            13: "Desert Mercenary - Defensive (Hell)",
            14: "Desert Mercenary - Offensive (Hell)",
            15: "Eastern Sorceror - Fire Spells (Normal)",
            16: "Eastern Sorceror - Cold Spells (Normal)",
            17: "Eastern Sorceror - Lightning Spells (Normal)",
            18: "Eastern Sorceror - Fire Spells (Nightmare)",
            19: "Eastern Sorceror - Cold Spells (Nightmare)",
            20: "Eastern Sorceror - Lightning Spells (Nightmare)",
            21: "Eastern Sorceror - Fire Spells (Hell)",
            22: "Eastern Sorceror - Cold Spells (Hell)",
            23: "Eastern Sorceror - Lightning Spells (Hell)",
            24: "Barbarian (Normal)",
            25: "Barbarian (Normal)",
            26: "Barbarian (Nightmare)",
            27: "Barbarian (Nightmare)",
            28: "Barbarian (Hell)",
            29: "Barbarian (Hell)",
        }
        return values[self.value]
