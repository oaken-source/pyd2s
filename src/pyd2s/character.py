
'''
this module provides a class that manages character data
'''

import re
import logging
from enum import Enum
from os.path import dirname, join, isfile

from pyd2s.gamedata import GameData


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
        return GameData.playerclass[self.value]['Code']

    def __str__(self):
        '''
        produce the title of the character class
        '''
        return GameData.get_string(f'partychar{self.code}')


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
        return GameData.get_string(GameData.skills[self.value]['skill'])


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


class Character:
    '''
    save data referring to the character itself
    '''

    class StatData:
        '''
        this class provides access to a characters stat data
        '''

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
                return int(GameData.itemstatcost[self.value]['CSvBits'])

        def __init__(self, buffer):
            '''
            constructor - propagate buffer and parse stats section
            '''
            self._buffer = buffer

            if self._header != 'gf':
                raise ValueError('invalid save: mismatched stat data section header')

            self._positions = {stat: None for stat in self.CharacterStat}
            self._end = 0
            self._stats_end = 0

            # if this is a sparse save file, we can stop looking for stat data
            if self._buffer.sparse:
                return

            ptr = self._buffer.BitReadPointer(self._buffer, 767 * 8)
            while True:
                statid = ptr.read_bits(9)
                if statid == 0x1FF:
                    break
                stat = self.CharacterStat(statid)
                self._positions[stat] = ptr.value
                value = ptr.read_bits(stat.bits)
                logging.debug('character:%s = %d', stat, value)
            self._end = ptr.value

        @property
        def _header(self):
            '''
            produce the header of the section - should be 'gf'
            '''
            if self._buffer.sparse:
                return 'gf'
            return self._buffer[765:767].decode('ascii')

        @property
        def length(self):
            '''
            the length of the stat section in bytes
            '''
            return (self._end - 1) // 8 + 1 - 765

        def __getitem__(self, statid):
            '''
            get the stat by id
            '''
            position = self._positions[statid]
            if position is None:
                return 0
            return self._buffer.getbits(position, statid.bits)

        def __setitem__(self, statid, value):
            '''
            set the stat by id to value
            '''
            if self._buffer.sparse:
                raise ValueError('unable to set stat data on sparse save.')

            if value.bit_length() > statid.bits:
                raise ValueError(f'value too large for stat {statid}')

            position = self._positions[statid]
            if position is None:
                # insert a new field after the end of the stats
                length = 9 + statid.bits
                logging.debug('StatData:appending stat with 9 + %d = %d bits length',
                              statid.bits, length)
                bits_over = length - (8 - self._end % 8) % 8
                logging.debug('StatData:%d bits over at _end %d (%d mod 8)',
                              bits_over, self._end, self._end % 8)
                bytes_over = (bits_over - 1) // 8 + 1
                logging.debug('StatData:allocating %d bytes over',
                              bytes_over)

                self._buffer.insert_bytes((self._end - 1) // 8 + 1, bytes_over)

                # override the last stat block end mark
                self._buffer.setbits(self._end - 9, statid.value, 9)
                # write the stat value
                self._buffer.setbits(self._end, value, statid.bits)
                # write the new stat block end mark
                self._buffer.setbits(self._end + statid.bits, 0x1ff, 9)

                # register the stat position and increase the length
                self._positions[statid] = self._end
                self._end += length
            else:
                self._buffer.setbits(position, value, statid.bits)

            # when updating the level, also update in the character data
            if statid == self.CharacterStat.LEVEL:
                self._buffer[43] = value

    class SkillData:
        '''
        this class provides access to a characters stat data
        '''

        def __init__(self, buffer, offset):
            '''
            constructor - propagate buffer and parse stats section
            '''
            self._buffer = buffer
            self._offset = buffer.dynamic_offset(offset)

            if self._header != 'if':
                raise ValueError('invalid save: mismatched skill data section header')

        @property
        def _header(self):
            '''
            produce the header of the section - should be 'if'
            '''
            if self._buffer.sparse:
                return 'if'
            return self._buffer[self._offset:self._offset + 2].decode('ascii')

        def __getitem__(self, skillid):
            '''
            get the skill by id
            '''
            if isinstance(skillid, SkillTree):
                skillid = skillid.value - skillid.offset()

            if self._buffer.sparse:
                return 0

            return self._buffer[self._offset + 2 + skillid]

        def __setitem__(self, skillid, value):
            '''
            set the skill by id to value
            '''
            if self._buffer.sparse:
                raise ValueError('unable to set skill data on sparse save.')

            if isinstance(skillid, SkillTree):
                skillid = skillid.value - skillid.offset

            self._buffer[self._offset + 2 + skillid] = value

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        logging.debug('Character:__init__')
        self._buffer = buffer

        GameData.set_expansion(self.is_expansion)

        self.stats = self.StatData(self._buffer)
        self.skills = self.SkillData(self._buffer, 765 + self.stats.length)

    @property
    def name(self):
        '''
        get the name of the character
        '''
        return self._buffer[20:36].decode('ascii').rstrip('\0')

    @name.setter
    def name(self, value):
        '''
        set the name of the character, this also updates save file locations
        '''
        if value == self.name:
            return

        if not re.fullmatch('(?=.{2,15})[a-zA-Z]+[-_]?[a-zA-Z]+', value):
            raise ValueError('character name is invalid')

        newpath = join(dirname(self._buffer.path), f"{value}.d2s")
        if isfile(newpath):
            raise ValueError('a character with this name already exists')

        self._buffer.path = newpath
        self._buffer[20:36] = value.ljust(16, '\0').encode('ascii')

    @property
    def is_expansion(self):
        '''
        True if an extension (LoD) character, False otherwise
        '''
        return (self._buffer[36] & (1 << 5)) != 0

    @property
    def has_died(self):
        '''
        True if the character has died in the past, False otherwise
        '''
        return (self._buffer[36] & (1 << 3)) != 0

    @has_died.setter
    def has_died(self, value):
        '''
        set wether the character has died in the past
        '''
        self._buffer[36] ^= (-bool(value) ^ self._buffer[36]) & (1 << 3)

    @property
    def is_hardcore(self):
        '''
        True if the character is a hardcore character, False otherwise
        '''
        return (self._buffer[36] & (1 << 2)) != 0

    @is_hardcore.setter
    def is_hardcore(self, value):
        '''
        set wether the character is a hardcore character
        '''
        self._buffer[36] ^= (-bool(value) ^ self._buffer[36]) & (1 << 2)

    @property
    def character_class(self):
        '''
        get the class of the character
        '''
        return CharacterClass(self._buffer[40])

    @character_class.setter
    def character_class(self, value):
        '''
        set the class of the character
        '''
        if not isinstance(value, CharacterClass):
            raise ValueError('character class is invalid')
        if value in (CharacterClass.ASSASSIN, CharacterClass.DRUID) and not self.is_expansion:
            raise ValueError('assassins and druids need expansion flag set')
        self._buffer[40] = value.value
