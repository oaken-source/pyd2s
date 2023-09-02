
'''
this module contains some basic enumerated types
'''

from enum import Enum
from functools import total_ordering


class TitledEnum(Enum):
    '''
    a base enum with a common string representation
    '''
    def __str__(self):
        '''
        a string representation converting the name to title case
        '''
        return self.name.replace('_', ' ').capitalize()


class SkillTree(TitledEnum):
    '''
    a base class of the skill tree
    '''
    @classmethod
    def for_class(cls, character_class):
        '''
        produce the appropriate skill tree for the given character class
        '''
        return {
            CharacterClass.AMAZON: AmazonSkillTree,
            CharacterClass.SORCERESS: SorceressSkillTree,
            CharacterClass.NECROMANCER: NecromancerSkillTree,
            CharacterClass.PALADIN: PaladinSkillTree,
            CharacterClass.BARBARIAN: BarbarianSkillTree,
            CharacterClass.DRUID: DruidSkillTree,
            CharacterClass.ASSASSIN: AssassinSkillTree,
        }[character_class]


class AmazonSkillTree(SkillTree):
    '''
    the skill tree of the amazon class
    '''
    MAGIC_ARROW = 0
    FIRE_ARROW = 1
    COLD_ARROW = 5
    MULTIPLE_SHOT = 6
    EXPLODING_ARROW = 10
    ICE_ARROW = 15
    GUIDED_ARROW = 16
    STRAFE = 20
    IMMOLATION_ARROW = 21
    FREEZING_ARROW = 25

    INNER_SIGHT = 2
    CRITICAL_STRIKE = 3
    DODGE = 7
    SLOW_MISSILES = 11
    AVOID = 12
    PENETRATE = 17
    DOPPLEZON = 22
    EVADE = 23
    VALKIRIE = 26
    PIERCE = 27

    JAB = 4
    POWER_STRIKE = 8
    POISON_JAVELIN = 9
    IMPALE = 13
    LIGHTNING_BOLT = 14
    CHARGED_STRIKE = 18
    PLAGUE_JAVELIN = 19
    FEND = 24
    LIGHTNING_STRIKE = 28
    LIGHTNING_FURY = 29


class SorceressSkillTree(SkillTree):
    '''
    the skill tree of the sorceress class
    '''
    FIRE_BOLT = 0
    WARMTH = 1
    INFERNO = 5
    BLAZE = 10
    FIRE_BALL = 11
    FIRE_WALL = 15
    ENCHANT = 16
    METEOR = 20
    FIRE_MASTERY = 25
    HYDRA = 26

    CHARGED_BOLT = 2
    STATIC_FIELD = 6
    TELEKINESIS = 7
    NOVA = 12
    LIGHTNING = 13
    CHAIN_LIGHTNING = 17
    TELEPORT = 18
    THUNDER_STORM = 21
    ENERGY_SHIELD = 22
    LIGHTNING_MASTERY = 27

    ICE_BOLT = 3
    FROZEN_ARMOR = 4
    FROST_NOVA = 8
    ICE_BLAST = 9
    SHIVER_ARMOR = 14
    GLACIAL_SPIKE = 19
    BLIZZARD = 23
    CHILLING_ARMOR = 24
    FROZEN_ORB = 28
    COLD_MASTERY = 29


class NecromancerSkillTree(SkillTree):
    '''
    the skill tree of the necromancer class
    '''
    AMPLIFY_DAMAGE = 0
    DIM_VISION = 5
    WEAKEN = 6
    IRON_MAIDEN = 10
    TERROR = 11
    CONFUSE = 15
    LIFE_TAP = 16
    ATTRACT = 20
    DECREPIFY = 21
    LOWER_RESIST = 25

    TEETH = 1
    BONE_ARMOR = 2
    POISON_DAGGER = 7
    CORPSE_EXPLOSION = 8
    BONE_WALL = 12
    POISON_EXPLOSION = 17
    BONE_SPEAR = 18
    BONE_PRISON = 22
    POISON_NOVA = 26
    BONE_SPIRIT = 27

    SKELETON_MASTERY = 3
    RAISE_SKELETON = 4
    CLAY_GOLEM = 9
    GOLEM_MASTERY = 13
    RAISE_SKELETAL_MAGE = 14
    BLOOD_GOLEM = 19
    SUMMON_RESIST = 23
    IRON_GOLEM = 24
    FIRE_GOLEM = 28
    REVIVE = 29


class PaladinSkillTree(SkillTree):
    '''
    the skill tree of the paladin class
    '''
    SACRIFICE = 0
    SMITE = 1
    HOLY_BOLT = 5
    ZEAL = 10
    CHARGE = 11
    VENGEANCE = 15
    BLESSED_HAMMER = 16
    CONVERSION = 20
    HOLY_SHIELD = 21
    FIST_OF_THE_HEAVENS = 25

    MIGHT = 2
    HOLY_FIRE = 6
    THORNS = 7
    BLESSED_AIM = 12
    CONCENTRATION = 17
    HOLY_FREEZE = 18
    HOLY_SHOCK = 22
    SANCTUARY = 23
    FANATICISM = 26
    CONVICTION = 27

    PRAYER = 3
    RESIST_FIRE = 4
    DEFIANCE = 8
    RESIST_COLD = 9
    CLEANSING = 13
    RESIST_LIGHTNING = 14
    VIGOR = 19
    MEDITATION = 24
    REDEMPTION = 28
    SALVATION = 29


class BarbarianSkillTree(SkillTree):
    '''
    the skill tree of the barbarian class
    '''
    BASH = 0
    LEAP = 6
    DOUBLE_SWING = 7
    STUN = 13
    DOUBLE_THROW = 14
    LEAP_ATTACK = 17
    CONCENTRATE = 18
    FRENZY = 21
    WHIRLWIND = 25
    BERSERK = 26

    SWORD_MASTERY = 1
    AXE_MASTERY = 2
    MACE_MASTERY = 3
    POLE_ARM_MASTERY = 8
    THROWING_MASTERY = 9
    SPEAR_MASTERY = 10
    INCREASED_STAMINA = 15
    IRON_SKIN = 19
    INCREASED_SPEED = 22
    NATURAL_RESISTANCE = 27

    HOWL = 4
    FIND_POTION = 5
    TAUNT = 11
    SHOUT = 12
    FIND_ITEM = 16
    BATTLE_CRY = 20
    BATTLE_ORDERS = 23
    GRIM_WARD = 24
    WAR_CRY = 28
    BATTLE_COMMAND = 29


class DruidSkillTree(SkillTree):
    '''
    the skill tree of the druid class
    '''
    RAVEN = 0
    PLAGUE_POPPY = 1
    OAK_SAGE = 5
    SUMMON_SPIRIT_WOLF = 6
    CYCLE_OF_LIFE = 10
    HEART_OF_WOLVERINE = 15
    SUMMON_FENRIS = 16
    VINES = 20
    SPIRIT_OF_BARBS = 25
    SUMMON_GRIZZLY = 26

    WEREWOLF = 2
    SHAPE_SHIFTING = 3
    WEREBEAR = 7
    FERAL_RAGE = 11
    MAUL = 12
    RABIES = 17
    FIRE_CLAWS = 18
    HUNGER = 21
    SHOCK_WAVE = 22
    FURY = 27

    FIRESTORM = 4
    MOLTEN_BOULDER = 8
    ARCIC_BLAST = 9
    ERUPTION = 13
    CYCLONE_ARMOR = 14
    TWISTER = 19
    VOLCANO = 23
    TORNADO = 24
    ARMAGEDDON = 28
    HURRICANE = 29


class AssassinSkillTree(SkillTree):
    '''
    the skill tree of the assassin class
    '''
    FIRE_TRAUMA = 0
    SHOCK_FIELD = 5
    BLADE_SENTINEL = 6
    CHARGED_BOLT_SENTRY = 10
    WAKE_OF_FIRE_SENTRY = 11
    BLADE_FURY = 15
    LIGHTNING_SENTRY = 20
    INFERNO_SENTRY = 21
    DEATH_SENTRY = 25
    BLADE_SHIELD = 26

    CLAW_MASTERY = 1
    PSYCHIC_HAMMER = 2
    QUICKNESS = 7
    WEAPON_BLOCK = 12
    CLOAK_OF_SHADOWS = 13
    FADE = 16
    SHADOW_WARRIOR = 17
    MIND_BLAST = 22
    VENOM = 27
    SHADOW_MASTER = 28

    TIGER_STRIKE = 3
    DRAGON_TALON = 4
    FISTS_OF_FIRE = 8
    DRAGON_CLAW = 9
    COBRA_STRIKE = 14
    CLAWS_OF_THUNDER = 18
    DRAGON_TAIL = 19
    BLADES_OF_ICE = 23
    DRAGON_FLIGHT = 24
    ROYAL_STRIKE = 29


class CharacterClass(TitledEnum):
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

    @property
    def skilltree(self):
        '''
        produce the skill tree of this class
        '''
        return SkillTree.for_class(self)


class CharacterStat(TitledEnum):
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


class Difficulty(TitledEnum):
    '''
    the difficulty levels available in the game
    '''
    NORMAL = 0x00
    NIGHTMARE = 0x01
    HELL = 0x02


class Act(TitledEnum):
    '''
    the acts available in the game
    '''
    ACT_1 = 0x00
    ACT_2 = 0x01
    ACT_3 = 0x02
    ACT_4 = 0x03
    ACT_5 = 0x04


class Waypoint(TitledEnum):
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


class Quest(TitledEnum):
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
            self.DEN_OF_EVIL: 2,
            self.SISTERS_BURIAL_GROUNDS: 4,
            self.TOOLS_OF_THE_TRADE: 6,
            self.THE_SEARCH_FOR_CAIN: 8,
            self.THE_FORGOTTEN_TOWER: 10,
            self.SISTERS_TO_THE_SLAUGHTER: 12,
            self.RADAMENTS_LAIR: 18,
            self.THE_HORADRIC_STAFF: 20,
            self.TAINTED_SUN: 22,
            self.ARCANE_SANCTUARY: 24,
            self.THE_SUMMONER: 26,
            self.THE_SEVEN_TOMBS: 28,
            self.LAM_ESENS_TOME: 34,
            self.KHALIMS_WILL: 36,
            self.BLADE_OF_THE_OLD_RELIGION: 38,
            self.THE_GOLDEN_BIRD: 40,
            self.THE_BLACKENED_TEMPLE: 42,
            self.THE_GUARDIAN: 44,
            self.THE_FALLEN_ANGEL: 50,
            self.TERRORS_END: 52,
            self.HELLS_FORGE: 54,
            self.SIEGE_OF_HARROGATH: 70,
            self.RESCUE_ON_MOUNT_ARREAT: 72,
            self.PRISON_OF_ICE: 74,
            self.BETRAYAL_OF_HARROGATH: 76,
            self.RITE_OF_PASSAGE: 78,
            self.EVE_OF_DESTRUCTION: 80,
        }[self]


@total_ordering
class ItemQuality(TitledEnum):
    '''
    an enum for possible item qualities
    '''
    LOW_QUALITY = 1
    NORMAL = 2
    HIGH_QUALITY = 3
    MAGICAL = 4
    SET = 5
    RARE = 6
    UNIQUE = 7
    CRAFTED = 8

    def __lt__(self, other):
        '''
        comparison for item qualities
        '''
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
