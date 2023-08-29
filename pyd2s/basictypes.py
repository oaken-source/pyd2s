
'''
this module contains some basic enumerated types
'''

from enum import Enum


class CharacterClass(Enum):
    '''
    the character classes available in the game
    '''
    AMAZON = 0x00
    SORCERESS = 0x01
    NECROMANCER = 0x02
    PALADIN = 0x03
    BARBARIAN = 0x04
    DRUID = 0x05
    ASSASSIN = 0x06

    def __str__(self):
        '''
        produce a string representation of this class
        '''
        return self.name.capitalize()


class CharacterStat(Enum):
    '''
    the character stat ids and bit widths
    '''
    STRENGTH = 0x00
    ENERGY = 0x01
    DEXTERITY = 0x02
    VITALITY = 0x03
    STATPTS = 0x04
    NEWSKILLS = 0x05
    HITPOINTS = 0x06
    MAXHP = 0x07
    MANA = 0x08
    MAXMANA = 0x09
    STAMINA = 0x0a
    MAXSTAMINA = 0x0b
    LEVEL = 0x0c
    EXPERIENCE = 0x0d
    GOLD = 0x0e
    GOLDBANK = 0x0f

    @property
    def bits(self):
        '''
        the bit width of the stat value
        '''
        return {
            self.STRENGTH: 10,
            self.ENERGY: 10,
            self.DEXTERITY: 10,
            self.VITALITY: 10,
            self.STATPTS: 10,
            self.NEWSKILLS: 8,
            self.HITPOINTS: 21,
            self.MAXHP: 21,
            self.MANA: 21,
            self.MAXMANA: 21,
            self.STAMINA: 21,
            self.MAXSTAMINA: 21,
            self.LEVEL: 7,
            self.EXPERIENCE: 32,
            self.GOLD: 25,
            self.GOLDBANK: 25,
        }[self]

    def __str__(self):
        '''
        a string representation of the stat
        '''
        return self.name.capitalize()


class Difficulty(Enum):
    '''
    the difficulty levels available in the game
    '''
    NORMAL = 0x00
    NIGHTMARE = 0x01
    HELL = 0x02

    def __str__(self):
        '''
        a string representation of the difficulty
        '''
        return self.name.capitalize()


class Act(Enum):
    '''
    the acts available in the game
    '''
    ACT_1 = 0x00
    ACT_2 = 0x01
    ACT_3 = 0x02
    ACT_4 = 0x03
    ACT_5 = 0x04

    def __str__(self):
        '''
        a string representation of the difficulty
        '''
        return self.name.replace('_', ' ').capitalize()


class Waypoint(Enum):
    '''
    the waypoints available in the game
    '''
    ROGUE_ENCAMPMENT = 0
    COLD_PLAINS = 1
    STONY_FIELD = 2
    DARK_WOOD = 3
    BLACK_MARSH = 4
    OUTER_CLOISTER = 5
    JAIL_LEVEL_1 = 6
    INNER_CLOISTER = 7
    CATACOMBS_LEVEL_2 = 8
    LUT_GHOLEIN = 9
    SEWERS_LEVEL_2 = 10
    DRY_HILLS = 11
    HALLS_OF_THE_DEAD_LEVEL_2 = 12
    FAR_OASIS = 13
    LOST_CITY = 14
    PALACE_CELLAR_LEVEL_1 = 15
    ARCANE_SANCTUARY = 16
    CANYON_OF_THE_MAGI = 17
    KURAST_DOCKS = 18
    SPIDER_FOREST = 19
    GREAT_MARSH = 20
    FLAYER_JUNGLE = 21
    LOWER_KURAST = 22
    KURAST_BAZAAR = 23
    UPPER_KURAST = 24
    TRAVINCAL = 25
    DURANCE_OF_HATE_LEVEL_2 = 26
    PANDEMONIUM_FORTRESS = 27
    CITY_OF_THE_DAMNED = 28
    RIVER_OF_FLAMES = 29
    HARROGATH = 30
    FRIGID_HIGHLANDS = 31
    ARREAT_PLATEAU = 32
    CRYSTALLINE_PASSAGE = 33
    HALLS_OF_PAIN = 34
    GLACIAL_TRAIL = 35
    FROZEN_TUNDRA = 36
    THE_ANCIENTS_WAY = 37
    WORLDSTONE_KEEP_LEVEL_2 = 38

    def __str__(self):
        '''
        a string representation of the difficulty
        '''
        return self.name.replace('_', ' ').title()


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
    SIEGE_OF_HARROGATH = 21
    RESCUE_ON_MOUNT_ARREAT = 22
    PRISON_OF_ICE = 23
    BETRAYAL_OF_HARROGATH = 24
    RITE_OF_PASSAGE = 25
    EVE_OF_DESTRUCTION = 26

    @property
    def offset(self):
        '''
        the offset of this quest into the quest data structure
        '''
        return {
            self.DEN_OF_EVIL : 2,
            self.SISTERS_BURIAL_GROUNDS : 4,
            self.TOOLS_OF_THE_TRADE : 6,
            self.THE_SEARCH_FOR_CAIN : 8,
            self.THE_FORGOTTEN_TOWER : 10,
            self.SISTERS_TO_THE_SLAUGHTER : 12,
            self.RADAMENTS_LAIR : 18,
            self.THE_HORADRIC_STAFF : 20,
            self.TAINTED_SUN : 22,
            self.ARCANE_SANCTUARY : 24,
            self.THE_SUMMONER : 26,
            self.THE_SEVEN_TOMBS : 28,
            self.LAM_ESENS_TOME : 34,
            self.KHALIMS_WILL : 36,
            self.BLADE_OF_THE_OLD_RELIGION : 38,
            self.THE_GOLDEN_BIRD : 40,
            self.THE_BLACKENED_TEMPLE : 42,
            self.THE_GUARDIAN : 44,
            self.THE_FALLEN_ANGEL : 50,
            self.TERRORS_END : 52,
            self.HELLS_FORGE : 54,
            self.SIEGE_OF_HARROGATH : 70,
            self.RESCUE_ON_MOUNT_ARREAT : 72,
            self.PRISON_OF_ICE : 74,
            self.BETRAYAL_OF_HARROGATH : 76,
            self.RITE_OF_PASSAGE : 78,
            self.EVE_OF_DESTRUCTION : 80,
        }[self]


    def __str__(self):
        '''
        a string representation of the quest type
        '''
        return self.name.replace('_', ' ').title()


class MercenaryTypes(Enum):
    '''
    the mercenary types available in the game
    '''
    ROGUE_FIRE_NORMAL = 0
    ROGUE_COLD_NORMAL = 1
    ROGUE_FIRE_NIGHTMARE = 2
    ROGUE_COLD_NIGHTMARE = 3
    ROGUE_FIRE_HELL = 4
    ROGUE_COLD_HELL = 5
    DESERT_COMBAT_NORMAL = 6
    DESERT_DEFENSIVE_NORMAL = 7
    DESERT_OFFENSIVE_NORMAL = 8
    DESERT_COMBAT_NIGHTMARE = 9
    DESERT_DEFENSIVE_NIGHTMARE = 10
    DESERT_OFFENSIVE_NIGHTMARE = 11
    DESERT_COMBAT_HELL = 12
    DESERT_DEFENSIVE_HELL = 13
    DESERT_OFFENSIVE_HELL = 14
    SORCEROR_FIRE_NORMAL = 15
    SORCEROR_COLD_NORMAL = 16
    SORCEROR_LIGHTNING_NORMAL = 17
    SORCEROR_FIRE_NIGHTMARE = 18
    SORCEROR_COLD_NIGHTMARE = 19
    SORCEROR_LIGHTNING_NIGHTMARE = 20
    SORCEROR_FIRE_HELL = 21
    SORCEROR_COLD_HELL = 22
    SORCEROR_LIGHTNING_HELL = 23
    BARBARIAN_NORMAL_A = 24
    BARBARIAN_NORMAL_B = 25
    BARBARIAN_NIGHTMARE_A = 26
    BARBARIAN_NIGHTMARE_B = 27
    BARBARIAN_HELL_A = 28
    BARBARIAN_HELL_B = 29

    @property
    def act(self):
        '''
        produce the act the mercenary was hired in
        '''
        if self.value < 6:
            return Act.ACT_1
        if self.value < 15:
            return Act.ACT_2
        if self.value < 24:
            return Act.ACT_3
        return Act.ACT_5

    @property
    def difficulty(self):
        '''
        produce the difficulty the mercenary was hired in
        '''
        if self.value in [0, 1, 6, 7, 8, 15, 16, 17, 24, 25]:
            return Difficulty.NORMAL
        if self.value in [2, 3, 9, 10, 11, 18, 19, 20, 26, 27]:
            return Difficulty.NIGHTMARE
        return Difficulty.HELL

    def __str__(self):
        '''
        produce a string representation of the Mercenary
        '''
        names = {
            Act.ACT_1: 'Rogue Scout',
            Act.ACT_2: 'Desert Mercenary',
            Act.ACT_3: 'Eastern Sorceror',
            Act.ACT_5: 'Barbarian',
        }
        types = {
            Act.ACT_1: ['Fire Arrow', 'Cold Arrow'],
            Act.ACT_2: ['Combat', 'Defensive', 'Offensive'],
            Act.ACT_3: ['Fire Spells', 'Cold Spells', 'Lightning Spells'],
        }

        res = f'{names[self.act]}'
        if self.act in types:
            res += f' - {types[self.act][self.value % len(types[self.act])]}'
        res += f' ({self.difficulty})'
        return res
