
'''
this module provides a class that manages skill data
'''

from pyd2s.basictypes import CharacterClass
from pyd2s.character import Character

D2_Skills = {
    0:"Attack",
    1:"Kick",
    2:"Throw",
    3:"Unsummon",
    4:"Left Hand Throw",
    5:"Left Hand Swing",

    6:"Magic Arrow",
    7:"Fire Arrow",
    8:"Inner Sight",
    9:"Critical Strike",
    10:"Jab",
    11:"Cold Arrow",
    12:"Multiple Shot",
    13:"Dodge",
    14:"Power Strike",
    15:"Poison Javelin",
    16:"Exploding Arrow",
    17:"Slow Missiles",
    18:"Avoid",
    19:"Impale",
    20:"Lightning Bolt",
    21:"Ice Arrow",
    22:"Guided Arrow",
    23:"Penetrate",
    24:"Charged Strike",
    25:"Plague Javelin",
    26:"Strafe",
    27:"Immolation Arrow",
    28:"Decoy",
    29:"Evade",
    30:"Fend",
    31:"Freezing Arrow",
    32:"Valkyrie",
    33:"Pierce",
    34:"Lightning Strike",
    35:"Lightning Fury",

    36:"Fire Bolt",
    37:"Warmth",
    38:"Charged Bolt",
    39:"Ice Bolt",
    40:"Frozen Armor",
    41:"Inferno",
    42:"Static Field",
    43:"Telekinesis",
    44:"Frost Nova",
    45:"Ice Blast",
    46:"Blaze",
    47:"Fire Ball",
    48:"Nova",
    49:"Lightning",
    50:"Shiver Armor",
    51:"Fire Wall",
    52:"Enchant",
    53:"Chain Lightning",
    54:"Teleport",
    55:"Glacial Spike",
    56:"Meteor",
    57:"Thunder Storm",
    58:"Energy Shield",
    59:"Blizzard",
    60:"Chilling Armor",
    61:"Fire Mastery",
    62:"Hydra",
    63:"Lightning Mastery",
    64:"Frozen Orb",
    65:"Cold Mastery",

    66:"Amplify Damage",
    67:"Teeth",
    68:"Bone Armor",
    69:"Skeleton Mastery",
    70:"Raise Skeleton",
    71:"Dim Vision",
    72:"Weaken",
    73:"Poison Dagger",
    74:"Corpse Explosion",
    75:"Clay Colem",
    76:"Iron Maiden",
    77:"Terror",
    78:"Bone Wall",
    79:"Golem Mastery",
    80:"Raise Skeletal Mage",
    81:"Confuse",
    82:"Life Tap",
    83:"Poison Explosion",
    84:"Bone Spear",
    85:"Blood Golem",
    86:"Attract",
    87:"Decrepify",
    88:"Bone Prison",
    89:"Summon Resist",
    90:"Iron Golem",
    91:"Lower Regist",
    92:"Poison Nova",
    93:"Bone Spirit",
    94:"Fire Golem",
    95:"Revive",

    96:"Sacrifice",
    97:"Smite",
    98:"Might",
    99:"Prayer",
    100:"Resist Fire",
    101:"Holy Bolt",
    102:"Holy Fire",
    103:"Throns",
    104:"Defiance",
    105:"Resist Cold",
    106:"Zeal",
    107:"Charge",
    108:"Blessed Aim",
    109:"Cleansing",
    110:"Resist Lightning",
    111:"Vengeance",
    112:"Blessed Hammer",
    113:"Concentration",
    114:"Holy Freeze",
    115:"Vigor",
    116:"Conversion",
    117:"Holy Shield",
    118:"Holy Shock",
    119:"Sanctuary",
    120:"Meditaion",
    121:"Fist of the Heavens",
    122:"Fanaticism",
    123:"Conviction",
    124:"Redemption",
    125:"Salvation",

    126:"Bash",
    127:"Sword Mastery",
    128:"Axe Mastery",
    129:"Mace Mastery",
    130:"Howl",
    131:"Find Potion",
    132:"Leap",
    133:"Double Swing",
    134:"Polearm Mastery",
    135:"Throwing Mastery",
    136:"Spear Mastery",
    137:"Taunt",
    138:"Shout",
    139:"Stun",
    140:"Double Throw",
    141:"Increased Stamina",
    142:"Find Item",
    143:"Leap Attack",
    144:"Concentrate",
    145:"Iron Skin",
    146:"Battle Cry",
    147:"Frenzy",
    148:"Increased Speed",
    149:"Battle Orders",
    150:"Grim Ward",
    151:"Whirlwind",
    152:"Berserk",
    153:"Natural Resistance",
    154:"War Cry",
    155:"Battle Command",

    217:"Scroll of Identify",
    218:"Tome of Identify",
    219:"Scroll of Town Portal",
    220:"Tome of Town Portal",

    221:"Raven",
    222:"Poison Creeper",
    223:"Wearwolf",
    224:"Lycanthropy",
    225:"Firestorm",
    226:"Oak Sage",
    227:"Summon Spirit Wolf",
    228:"Wearbear",
    229:"Molten Boulder",
    230:"Arctic Blast",
    231:"Carrion Vine",
    232:"Feral Rage",
    233:"Maul",
    234:"Fissure",
    235:"Cyclone Armor",
    236:"Heart of Wolverine",
    237:"Summon Dire Wolf",
    238:"Rabies",
    239:"Fire Claws",
    240:"Twister",
    241:"Solar Creeper",
    242:"Hunger",
    243:"Shock Wave",
    244:"Volcano",
    245:"Tornado",
    246:"Spirit of Barbs",
    247:"Summon Grizzly",
    248:"Fury",
    249:"Armageddon",
    250:"Hurricane",

    251:"Fire Blast",
    252:"Claw Mastery",
    253:"Psychic Hammer",
    254:"Tiger Strike",
    255:"Dragon Talon",
    256:"Shock Web",
    257:"Blade Sentinel",
    258:"Burst of Speed",
    259:"Fist of Fire",
    260:"Dragon Claw",
    261:"Charged Bolt Sentry",
    262:"Wake of Fire",
    263:"Weapon Block",
    264:"Cloak of Shadows",
    265:"Cobra Strike",
    266:"Blade Fury",
    267:"Fade",
    268:"Shadow Warrior",
    269:"Claws of Thunder",
    270:"Dragon Tail",
    271:"Lightning Sentry",
    272:"Wake of Inferno",
    273:"Mind Blast",
    274:"Blades of Ice",
    275:"Dragon Flight",
    276:"Death Sentry",
    277:"Blade Shield",
    278:"Venom",
    279:"Shadow Master",
    280:"Phoenix Strike",
}

D2_SkillsOrder_Amazon = [
    4, 8, 9, 13, 14, 18, 19, 24, 28, 29,
    2, 3, 7, 11, 12, 17, 22, 23, 26, 27,
    0, 1, 5, 6, 10, 15, 16, 21, 20, 25
]
D2_SkillsOrder_Sorceress = [
    3, 4, 8, 9, 14, 19, 23, 24, 28, 29,
    2, 7, 6, 13, 12, 17, 18, 21, 22, 27,
    0, 1, 5, 10, 11, 15, 16, 20, 25, 26
]
D2_SkillsOrder_Necromancer = [
    4, 3, 9, 13, 14, 19, 23, 24, 28, 29,
    1, 2, 7, 8, 12, 17, 18, 22, 26, 27,
    0, 5, 6, 10, 11, 15, 16, 20, 21, 25
]
D2_SkillsOrder_Paladin = [
    3, 4, 9, 8, 14, 13, 19, 24, 28, 29,
    2, 6, 7, 12, 17, 18, 22, 23, 26, 27,
    0, 1, 5, 10, 11, 15, 16, 20, 21, 25
]
D2_SkillsOrder_Barbarian = [
    4, 5, 12, 11, 16, 20, 23, 24, 28, 29,
    1, 2, 3, 8, 9, 10, 15, 19, 22, 27,
    0, 7, 6, 14, 13, 17, 18, 21, 25, 26
]
D2_SkillsOrder_Druid = [
    4, 8, 9, 14, 13, 19, 23, 24, 29, 28,
    2, 3, 7, 12, 11, 18, 17, 22, 21, 27,
    0, 1, 5, 6, 10, 15, 16, 20, 25, 26
]
D2_SkillsOrder_Assassin = [
    3, 4, 8, 9, 14, 18, 19, 23, 24, 29,
    1, 2, 7, 13, 12, 16, 17, 22, 27, 28,
    0, 5, 6, 10, 11, 15, 20, 21, 25, 26
]

D2_SkillsOrder = [
    D2_SkillsOrder_Amazon,
    D2_SkillsOrder_Sorceress,
    D2_SkillsOrder_Necromancer,
    D2_SkillsOrder_Paladin,
    D2_SkillsOrder_Barbarian,
    D2_SkillsOrder_Druid,
    D2_SkillsOrder_Assassin
]

class Skill(object):
    '''
    save data referring to the skill
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer

        self._character = Character(self._buffer)

        self._class = self._character.character_class
        self._newskills = self._character.newskills

        ifstart = 816

        if self._class == CharacterClass.Amazon:
            self._idstart = 6
        elif self._class == CharacterClass.Sorceress:
            self._idstart = 36
        elif self._class == CharacterClass.Necromancer:
            self._idstart = 66
        elif self._class == CharacterClass.Paladin:
            self._idstart = 96
        elif self._class == CharacterClass.Barbarian:
            self._idstart = 126
        elif self._class == CharacterClass.Druid:
            self._idstart = 221
        elif self._class == CharacterClass.Assassin:
            self._idstart = 251

        self._skillpoints = []

        for i in range(30):
            j = self._buffer[ifstart + i]
            self._skillpoints.append(j)

    def getclass(self):
        '''
        get character class
        '''
        return self._class

    def getskillpoints(self, idx):
        '''
        get skill points
        '''
        if idx >= 30:
            return 0
        return self._skillpoints[idx]

    def getskillname(self, idx):
        '''
        get skill name
        '''
        if idx >= 30:
            return 0
        return D2_Skills[self._idstart + idx]

    def getnewskills(self):
        '''
        get new skill points
        '''
        return self._newskills

