
'''
this module contains some basic enumerated types
'''

from enum import Enum
from functools import total_ordering

from pyd2s.gamedata import GameData


class SkillTree(Enum):
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

    @classmethod
    def offset(cls):
        '''
        produce the offset of the skill tree
        '''
        return min(skill.value for skill in cls)

    def __str__(self):
        '''
        produce the title of the skill
        '''
        return GameData.skills[self.value]['skill']


class AmazonSkillTree(SkillTree):
    '''
    the skill tree of the amazon class
    '''
    MAGIC_ARROW = 6
    FIRE_ARROW = 7
    COLD_ARROW = 11
    MULTIPLE_SHOT = 12
    EXPLODING_ARROW = 16
    ICE_ARROW = 21
    GUIDED_ARROW = 22
    STRAFE = 26
    IMMOLATION_ARROW = 27
    FREEZING_ARROW = 31

    INNER_SIGHT = 8
    CRITICAL_STRIKE = 9
    DODGE = 13
    SLOW_MISSILES = 17
    AVOID = 18
    PENETRATE = 23
    DOPPLEZON = 28
    EVADE = 29
    VALKIRIE = 32
    PIERCE = 33

    JAB = 10
    POWER_STRIKE = 14
    POISON_JAVELIN = 15
    IMPALE = 19
    LIGHTNING_BOLT = 20
    CHARGED_STRIKE = 24
    PLAGUE_JAVELIN = 25
    FEND = 30
    LIGHTNING_STRIKE = 34
    LIGHTNING_FURY = 35


class SorceressSkillTree(SkillTree):
    '''
    the skill tree of the sorceress class
    '''
    FIRE_BOLT = 36
    WARMTH = 37
    INFERNO = 41
    BLAZE = 46
    FIRE_BALL = 47
    FIRE_WALL = 51
    ENCHANT = 52
    METEOR = 56
    FIRE_MASTERY = 61
    HYDRA = 62

    CHARGED_BOLT = 38
    STATIC_FIELD = 42
    TELEKINESIS = 43
    NOVA = 48
    LIGHTNING = 49
    CHAIN_LIGHTNING = 53
    TELEPORT = 54
    THUNDER_STORM = 57
    ENERGY_SHIELD = 58
    LIGHTNING_MASTERY = 63

    ICE_BOLT = 39
    FROZEN_ARMOR = 40
    FROST_NOVA = 44
    ICE_BLAST = 45
    SHIVER_ARMOR = 50
    GLACIAL_SPIKE = 55
    BLIZZARD = 59
    CHILLING_ARMOR = 60
    FROZEN_ORB = 64
    COLD_MASTERY = 65


class NecromancerSkillTree(SkillTree):
    '''
    the skill tree of the necromancer class
    '''
    AMPLIFY_DAMAGE = 66
    DIM_VISION = 71
    WEAKEN = 72
    IRON_MAIDEN = 76
    TERROR = 77
    CONFUSE = 81
    LIFE_TAP = 82
    ATTRACT = 86
    DECREPIFY = 87
    LOWER_RESIST = 91

    TEETH = 67
    BONE_ARMOR = 68
    POISON_DAGGER = 73
    CORPSE_EXPLOSION = 74
    BONE_WALL = 78
    POISON_EXPLOSION = 83
    BONE_SPEAR = 84
    BONE_PRISON = 88
    POISON_NOVA = 92
    BONE_SPIRIT = 93

    SKELETON_MASTERY = 69
    RAISE_SKELETON = 70
    CLAY_GOLEM = 75
    GOLEM_MASTERY = 79
    RAISE_SKELETAL_MAGE = 80
    BLOOD_GOLEM = 85
    SUMMON_RESIST = 89
    IRON_GOLEM = 90
    FIRE_GOLEM = 94
    REVIVE = 95


class PaladinSkillTree(SkillTree):
    '''
    the skill tree of the paladin class
    '''
    SACRIFICE = 96
    SMITE = 97
    HOLY_BOLT = 101
    ZEAL = 106
    CHARGE = 107
    VENGEANCE = 111
    BLESSED_HAMMER = 112
    CONVERSION = 116
    HOLY_SHIELD = 117
    FIST_OF_THE_HEAVENS = 121

    MIGHT = 98
    HOLY_FIRE = 102
    THORNS = 103
    BLESSED_AIM = 108
    CONCENTRATION = 113
    HOLY_FREEZE = 114
    HOLY_SHOCK = 118
    SANCTUARY = 119
    FANATICISM = 122
    CONVICTION = 123

    PRAYER = 99
    RESIST_FIRE = 100
    DEFIANCE = 104
    RESIST_COLD = 105
    CLEANSING = 109
    RESIST_LIGHTNING = 110
    VIGOR = 115
    MEDITATION = 120
    REDEMPTION = 124
    SALVATION = 125


class BarbarianSkillTree(SkillTree):
    '''
    the skill tree of the barbarian class
    '''
    BASH = 126
    LEAP = 132
    DOUBLE_SWING = 133
    STUN = 139
    DOUBLE_THROW = 140
    LEAP_ATTACK = 143
    CONCENTRATE = 144
    FRENZY = 147
    WHIRLWIND = 151
    BERSERK = 152

    SWORD_MASTERY = 127
    AXE_MASTERY = 128
    MACE_MASTERY = 129
    POLE_ARM_MASTERY = 134
    THROWING_MASTERY = 135
    SPEAR_MASTERY = 136
    INCREASED_STAMINA = 141
    IRON_SKIN = 145
    INCREASED_SPEED = 148
    NATURAL_RESISTANCE = 153

    HOWL = 130
    FIND_POTION = 131
    TAUNT = 137
    SHOUT = 138
    FIND_ITEM = 142
    BATTLE_CRY = 146
    BATTLE_ORDERS = 149
    GRIM_WARD = 150
    WAR_CRY = 154
    BATTLE_COMMAND = 155


class DruidSkillTree(SkillTree):
    '''
    the skill tree of the druid class
    '''
    RAVEN = 221
    PLAGUE_POPPY = 222
    OAK_SAGE = 226
    SUMMON_SPIRIT_WOLF = 227
    CYCLE_OF_LIFE = 231
    HEART_OF_WOLVERINE = 236
    SUMMON_FENRIS = 237
    VINES = 241
    SPIRIT_OF_BARBS = 246
    SUMMON_GRIZZLY = 247

    WEREWOLF = 223
    SHAPE_SHIFTING = 224
    WEREBEAR = 228
    FERAL_RAGE = 232
    MAUL = 233
    RABIES = 238
    FIRE_CLAWS = 239
    HUNGER = 242
    SHOCK_WAVE = 243
    FURY = 248

    FIRESTORM = 225
    MOLTEN_BOULDER = 229
    ARCIC_BLAST = 230
    ERUPTION = 234
    CYCLONE_ARMOR = 235
    TWISTER = 240
    VOLCANO = 244
    TORNADO = 245
    ARMAGEDDON = 249
    HURRICANE = 250


class AssassinSkillTree(SkillTree):
    '''
    the skill tree of the assassin class
    '''
    FIRE_TRAUMA = 251
    SHOCK_FIELD = 256
    BLADE_SENTINEL = 257
    CHARGED_BOLT_SENTRY = 261
    WAKE_OF_FIRE_SENTRY = 262
    BLADE_FURY = 266
    LIGHTNING_SENTRY = 271
    INFERNO_SENTRY = 272
    DEATH_SENTRY = 276
    BLADE_SHIELD = 277

    CLAW_MASTERY = 252
    PSYCHIC_HAMMER = 253
    QUICKNESS = 258
    WEAPON_BLOCK = 263
    CLOAK_OF_SHADOWS = 264
    FADE = 267
    SHADOW_WARRIOR = 268
    MIND_BLAST = 273
    VENOM = 278
    SHADOW_MASTER = 279

    TIGER_STRIKE = 254
    DRAGON_TALON = 255
    FISTS_OF_FIRE = 259
    DRAGON_CLAW = 260
    COBRA_STRIKE = 265
    CLAWS_OF_THUNDER = 269
    DRAGON_TAIL = 270
    BLADES_OF_ICE = 274
    DRAGON_FLIGHT = 275
    ROYAL_STRIKE = 280


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

    @property
    def skilltree(self):
        '''
        produce the skill tree of this class
        '''
        return SkillTree.for_class(self)

    @property
    def code(self):
        '''
        produce the short code of the character class
        '''
        return {
            self.AMAZON: 'ama',
            self.SORCERESS: 'sor',
            self.NECROMANCER: 'nec',
            self.PALADIN: 'pal',
            self.BARBARIAN: 'bar',
            self.DRUID: 'dru',
            self.ASSASSIN: 'ass',
        }[self]

    def __str__(self):
        '''
        produce the title of the character class
        '''
        return GameData.get_string(f'partychar{self.code}')


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


@total_ordering
class ItemQuality(Enum):
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
