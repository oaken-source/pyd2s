'''
this module provides classes for item enhancements and properties
'''

from pyd2s.gamedata import GameData


# get stat groups from game data
STAT_GROUPS = [
    {
        'dgrp': [
            stat['Stat'] for stat in GameData.itemstatcost if stat['dgrp'] == group_id],
        'dgrpfunc': int(next(
            stat['dgrpfunc'] for stat in GameData.itemstatcost if stat['dgrp'] == group_id)),
        'dgrpstrpos': next(
            stat['dgrpstrpos'] for stat in GameData.itemstatcost if stat['dgrp'] == group_id),
        'dgrpstrneg': next(
            stat['dgrpstrneg'] for stat in GameData.itemstatcost if stat['dgrp'] == group_id),
    }
    for group_id in set(
        stat['dgrp'] for stat in GameData.itemstatcost if stat['dgrp'])
]

STAT_GROUPS.extend([
    {
        'dgrp': ['firemindam', 'firemaxdam'],
        'dgrpfunc': 30,
        'dgrpstrpos': 'strModFireDamageRange',
        'dgrgstrneg': 'strModFireDamageRange',
    },
    {
        'dgrp': ['lightmindam', 'lightmaxdam'],
        'dgrpfunc': 30,
        'dgrpstrpos': 'strModLightningDamageRange',
        'dgrgstrneg': 'strModLightningDamageRange',
    },
    {
        'dgrp': ['coldmindam', 'coldmaxdam', 'coldlength'],
        'dgrpfunc': 30,
        'dgrpstrpos': 'strModColdDamageRange',
        'dgrgstrneg': 'strModColdDamageRange',
    },
    {
        'dgrp': ['poisonmindam', 'poisonmaxdam', 'poisonlength'],
        'dgrpfunc': 31,
        'dgrpstrpos': 'strModPoisonDamageRange',
        'dgrgstrneg': 'strModPoisonDamageRange',
    },
    {
        'dgrp': ['maxdamage', 'secondary_maxdamage'],
        'dgrpfunc': 1,
        'dgrpstrpos': 'ModStr1f',
        'dgrgstrneg': 'ModStr1f',
    },
])

STAT_GROUPS_INDEX = {
    stat: group
    for group in STAT_GROUPS
    for stat in group['dgrp']
}


class ItemStat:
    '''
    a magical item enhancement
    '''
    def __init__(self, code, param, value):
        '''
        constructor
        '''
        if isinstance(code, str):
            self._itemstat = GameData.itemstatcost_index[code]
        else:
            self._itemstat = GameData.itemstatcost[code]

        self._param = param
        self._value = value

        self._children = []

    @property
    def stat(self):
        '''
        the string id of the stat
        '''
        return self._itemstat['Stat']

    @property
    def stat_id(self):
        '''
        the numerical id of the stat
        '''
        return int(self._itemstat['ID'])

    @property
    def value(self):
        '''
        the value of the stat
        '''
        return self._value

    @property
    def is_visible(self):
        '''
        indicate whether the property has a desc_func
        '''
        return bool(self._itemstat['descfunc'])

    @property
    def param(self):
        '''
        the param of the stat
        '''
        return self._param

    def add_child(self, child):
        '''
        add a child property
        '''
        self._children.append(child)

    def group_with(self, others):
        '''
        attempt to group two item stat blocks together into one
        '''
        if self.stat not in STAT_GROUPS_INDEX:
            return 0

        group = STAT_GROUPS_INDEX[self.stat]

        match = [self]
        for other in others:
            if other.stat not in group['dgrp']:
                break
            match.append(other)

        group_set = set(group['dgrp'])
        match_set = set(other.stat for other in match)

        if group_set != match_set:
            return 0

        for other in match[1:]:
            self.add_child(other)

        return len(match) - 1

    def __lt__(self, other):
        '''
        comparator used for sorting
        '''
        if self.__class__ is other.__class__:
            if self.stat == other.stat == 'item_singleskill':
                self_skill = GameData.skills[self.param]
                other_skill = GameData.skills[other.param]
                return int(self_skill['Id']) < int(other_skill['Id'])
            return (int(self._itemstat['descpriority'] or 0)
                    < int(other._itemstat['descpriority'] or 0))
        return NotImplemented

    def __str__(self):
        '''
        a string representation of the magical enhancement
        '''
        # determine formatter for individual stat
        desc_func = int(self._itemstat['descfunc'])
        str1 = self._itemstat['descstrpos'] if self.value >= 0 else self._itemstat['descstrneg']

        # determine if we're grouping to a common description
        if self.stat in STAT_GROUPS_INDEX:
            group = STAT_GROUPS_INDEX[self.stat]
            local = set(
                [self.stat] + [child.stat for child in self._children])
            other = set(group['dgrp'])

            if local == other:
                desc_func = group['dgrpfunc']
                str1 = group['dgrpstrpos'] if self.value >= 0 else group['dgrpstrneg']

        # special cases
        if self.stat == 'item_maxdamage_percent':
            # this is coded in the game files completely differently than displayed in-game
            desc_func = 4
            self._itemstat['descval'] = '1'
            str1 = 'Enhanced Damage'

        # otherwise dispatch to formatter by desc_func id
        try:
            formatter = getattr(self, f'_str_formatter_{desc_func}')
        except AttributeError as exc:
            raise NotImplementedError(f'_str_formatter_{desc_func}') from exc
        return formatter(str1)

    def _order_by_descval(self, line, value):
        '''
        determine the order of string components by descval setting
        '''
        if self._itemstat['descval'] == '1':
            # value comes first
            return value + ' ' + line
        if self._itemstat['descval'] == '2':
            # value comes last
            return line + ' ' + value
        # value is ignored
        return line

    # below are the item property formatters known from the game. this may be incomplete, I
    # will add the missing ones as I come across items that use these functions. If you come
    # across an item that is not covered here, please use the test-case generation function
    # of pyd2s_stat to create a test case and submit an issue or pull request.

    def _str_formatter_1(self, str1):
        '''
        +[value] [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'+{self.value}'
        return self._order_by_descval(line, value)

    def _str_formatter_2(self, str1):
        '''
        [value]% [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value}%'
        return self._order_by_descval(line, value)

    def _str_formatter_3(self, str1):
        '''
        [value] [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value}'
        return self._order_by_descval(line, value)

    def _str_formatter_4(self, str1):
        '''
        +[value]% [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'+{self.value}%'
        return self._order_by_descval(line, value)

    def _str_formatter_5(self, str1):
        '''
        [value]% [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{round(self.value * 100 / 128)}%'
        return self._order_by_descval(line, value)

#     6 - +[value] [string1] [string2]
#     7 - [value]% [string1] [string2]
#     8 - +[value]% [string1] [string2]
#     9 - [value] [string1] [string2]
#    10 - [value*100/128]% [string1] [string2]

    def _str_formatter_11(self, str1):
        '''
        Repairs 1 Durability In [100 / value] Seconds
        '''
        return GameData.get_string(str1) % (1, 100 // self.value)

#    12 - +[value] [string1]
#    13 - +[value] to [class] Skill Levels
#    14 - +[value] to [skilltab] Skill Levels ([class] Only)

    def _str_formatter_15(self, str1):
        '''
        [chance]% to case [slvl] [skill] on [event]
        '''
        skill_data = GameData.skills[self.param >> 6]
        skill_desc = GameData.skilldesc[skill_data['skilldesc']]
        skill_name = GameData.get_string(skill_desc['str name'])
        return GameData.get_string(str1) % (self.value, self.param & 0b111111, skill_name)

#    16 - Level [sLvl] [skill] Aura When Equipped
#    17 - [value] [string1] (Increases near [time])
#    18 - [value]% [string1] (Increases near [time])

    def _str_formatter_19(self, str1):
        '''
        this is used by stats that use Blizzard's sprintf implementation
        '''
        return GameData.get_string(str1) % (self.value, )

    def _str_formatter_20(self, str1):
        '''
        [value * -1]% [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value * -1}%'
        return self._order_by_descval(line, value)

    def _str_formatter_21(self, str1):
        '''
        [value * -1] [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value * -1}'
        return self._order_by_descval(line, value)

#    22 - [value]% [string1] [montype] (warning: this is bugged in vanilla and
#         doesn't work properly, see CE forum)
#    23 - [value]% [string1] [monster]
#    24 - used for charges, we all know how that desc looks
#    25 - not used by vanilla, present in the code but I didn't test it yet
#    26 - not used by vanilla, present in the code but I didn't test it yet

    def _str_formatter_27(self, _):
        '''
        +[value] to [skill] ([class] Only)
        '''
        skill_data = GameData.skills[self.param]
        skill_desc = GameData.skilldesc[skill_data['skilldesc']]
        skill_name = GameData.get_string(skill_desc['str name'])
        character_class = GameData.get_string("partychar" + skill_data["charclass"])
        # there seems to be no string constant for this one
        return f'+{self.value} to {skill_name} ({character_class} Only)'

#    28 - +[value] to [skill]

    # the official formatters end here, the following are helpers introduced for
    # custom skill groups that are not part of the data files but seem to be
    # hard coded in the game instead.

    def _str_formatter_30(self, str1):
        '''
        non-poison-damage type grouping
        '''
        mindam = self.value
        maxdam = self._children[0].value

        args = (mindam, maxdam)

        if mindam == maxdam:
            str1 = str1.removesuffix('Range')
            args = args[::2]

        return GameData.get_string(str1) % args

    def _str_formatter_31(self, str1):
        '''
        poison-damage type grouping
        '''
        mindam = self.value
        maxdam = self._children[0].value
        length = self._children[1].value

        args = (
            round(mindam / 256 * length),
            round(maxdam / 256 * length),
            round(length / 25))

        if mindam == maxdam:
            str1 = str1.removesuffix('Range')
            args = args[::2]

        return GameData.get_string(str1) % args


class ItemProperty:
    '''
    a property on a socketable item
    '''
    def __init__(self, code, param, min_value, max_value):
        '''
        constructor
        '''
        self._code = code
        self._param = param
        self._min_value = min_value
        self._max_value = max_value

        self._property = GameData.properties[self._code]

        # this property has no stat assigned
        if self._code == 'dmg-max':
            self._property['stat1'] = 'maxdamage'

        self._itemstat = ItemStat(self._property['stat1'], param, min_value)
        for i in range(2, 8):
            if self._property[f'stat{i}']:
                self._itemstat.add_child(ItemStat(self._property[f'stat{i}'], param, max_value))

    @property
    def itemstat(self):
        '''
        produce the ItemStat of this property
        '''
        return self._itemstat

    def group_with(self, others):
        '''
        group the current property with the next one, return true if successful
        '''
        return self.itemstat.group_with(other.itemstat for other in others)

    def __lt__(self, other):
        '''
        comparator used for sorting
        '''
        if self.__class__ is other.__class__:
            return self._itemstat < other._itemstat
        return NotImplemented

    def __str__(self):
        '''
        a string representation of the property
        '''
        return str(self._itemstat)