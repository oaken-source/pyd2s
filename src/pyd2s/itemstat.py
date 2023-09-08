'''
this module provides classes for item enhancements and properties
'''

import logging

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

# extend with more groups hard-coded in the game
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
    {
        'dgrp': ['mindamage', 'secondary_mindamage'],
        'dgrpfunc': 1,
        'dgrpstrpos': 'ModStr1g',
        'dgrgstrneg': 'ModStr1g',
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
    @classmethod
    def read_list(cls, ptr):
        '''
        read a list of ItemStat instances from a SaveBuffer pointer
        '''
        res = []

        while True:
            eid = ptr.read_bits(9)
            if eid == 0x1FF:
                break

            # some item stats expect more data blocks without explicit eid's
            consecutive = GameData.get_consecutive_item_stat_blocks(eid)

            group = []
            for _eid in range(eid, eid + consecutive):
                item_stat_cost = GameData.itemstatcost[_eid]

                field_width = int(item_stat_cost['Save Param Bits'] or 0)
                param = ptr.read_bits(field_width)

                field_width = int(item_stat_cost['Save Bits'] or 0)
                value = ptr.read_bits(field_width)
                value -= int(item_stat_cost['Save Add'] or 0)

                group.append(ItemStat(_eid, param, value))

            for child in group[1:]:
                group[0].add_child(child)

            res.append(group[0])

        return list(cls.group_reduce(res))

    @classmethod
    def group_reduce(cls, iterable):
        '''
        reduce the property list into groups
        '''
        elements = list(iterable)
        res = []
        i = 0
        while i < len(elements):
            element = elements[i]
            i += 1
            i += element.group_with(elements[i:])
            res.append(element)
        return res

    def __init__(self, code, param, value):
        '''
        constructor
        '''
        if isinstance(code, str):
            self._itemstat = GameData.itemstatcost_index[code]
        else:
            self._itemstat = GameData.itemstatcost[code]

        # if we don't have a param, use the value instead. this is useful in cases
        # where mods and properties follow differnt conventions for encoding values
        # for example with poisonlength.
        self._param = param if param else value
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
        if self._itemstat['op']:
            # little benefit to deviate from the original names just to placate pylint
            # pylint: disable=C0103
            op = int(self._itemstat['op'] or 0)
            op_param = int(self._itemstat['op param'] or 0)

            logging.debug(self._itemstat)

            if op in [2, 4]:
                return self._value / (2 ** op_param)

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

    @property
    def applies_to(self):
        '''
        indicate whether the modifier applies to the given stat
        '''
        stats = [
            self._itemstat['Stat'],
            *(
                self._itemstat[f'op stat{i}']
                for i in range(1, 4) if self._itemstat[f'op stat{i}']),
            *(stat for child in self._children for stat in child.applies_to)]
        return stats

    def apply_to(self, base_value):
        '''
        modify the given value by this stat and return the bonus
        '''
        # little benefit to deviate from the original names just to placate pylint
        # pylint: disable=C0103
        op = int(self._itemstat['op'] or 0)

        if op == 0:
            return self.value
        if op in [2, 4]:
            # conversion already covered in value property
            return self.value
        if op == 13:
            return base_value * self.value // 100

        raise NotImplementedError(op)

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
        if not self._itemstat['descfunc']:
            return ''

        # determine formatter for individual stat
        desc_func = int(self._itemstat['descfunc'])
        str1 = self._itemstat['descstrpos'] if self.value >= 0 else self._itemstat['descstrneg']
        str2 = self._itemstat['descstr2']

        logging.debug('ItemStat.__str__:item_stat: %s', self._itemstat)
        logging.debug('ItemStat.__str__:value: %s (%s)', self.value, self._value)
        logging.debug('ItemStat.__str__:param: %s', self.param)
        logging.debug('ItemStat.__str__:desc_func: %d', desc_func)
        logging.debug('ItemStat.__str__:str1: %s', str1)
        logging.debug('ItemStat.__str__:str2: %s', str2)

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
        return formatter(str1, str2)

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

    def _str_formatter_1(self, str1, _):
        '''
        1 - +[value] [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value:+}'
        return self._order_by_descval(line, value)

    def _str_formatter_2(self, str1, _):
        '''
        2 - [value]% [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value}%'
        return self._order_by_descval(line, value)

    def _str_formatter_3(self, str1, _):
        '''
        3 - [value] [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value}'
        return self._order_by_descval(line, value)

    def _str_formatter_4(self, str1, _):
        '''
        4 - +[value]% [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value:+}%'
        return self._order_by_descval(line, value)

    def _str_formatter_5(self, str1, _):
        '''
        5 - [value]% [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{round(self.value * 100 / 128)}%'
        return self._order_by_descval(line, value)

    def _str_formatter_6(self, str1, str2):
        '''
        6 - +[value] [string1] [string2]
        '''

        line = f'{GameData.get_string(str1)} {GameData.get_string(str2)}'
        value = f'{self.value:+}'
        return self._order_by_descval(line, value)

#     7 - [value]% [string1] [string2]
#     8 - +[value]% [string1] [string2]
#     9 - [value] [string1] [string2]
#    10 - [value*100/128]% [string1] [string2]

    def _str_formatter_11(self, str1, _):
        '''
        11 - Repairs 1 Durability In [100 / value] Seconds
        '''
        return GameData.get_string(str1) % (1, 100 // self.value)

    def _str_formatter_12(self, str1, _):
        '''
        12 - +[value] [string1]
        '''
        # this is only used by item_stupidity and item_freeze
        # value is only printed if >1
        line = GameData.get_string(str1)
        value = f'{self.value:+}'
        if self.value > 1:
            return self._order_by_descval(line, value)
        return line

    def _str_formatter_13(self, *_):
        '''
        13 - +[value] to [class] Skill Levels
        '''
        # str1 is misleading. instead, grab from charstats.txt
        str1 = GameData.charstats[self._param]['StrAllSkills']
        return f'{self.value:+} {GameData.get_string(str1)}'

    def _str_formatter_14(self, *_):
        '''
        14 - +[value] to [skilltab] Skill Levels ([class] Only)
        '''
        # str1 is misleading. instead, grab from charstats.txt
        charstats = GameData.charstats[self._param >> 3]
        str1 = charstats[f'StrSkillTab{(self._param & 0x7) + 1}']
        str2 = GameData.get_string(charstats['StrClassOnly'])
        return GameData.get_string(str1) % self._value + ' ' + str2

    def _str_formatter_15(self, str1, _):
        '''
        15 - [chance]% to case [slvl] [skill] on [event]
        '''
        skill_data = GameData.skills[self.param >> 6]
        skill_desc = GameData.skilldesc[skill_data['skilldesc']]
        skill_name = GameData.get_string(skill_desc['str name'])
        return GameData.get_string(str1) % (self.value, self.param & 0b111111, skill_name)

#    16 - Level [sLvl] [skill] Aura When Equipped
#    17 - [value] [string1] (Increases near [time])
#    18 - [value]% [string1] (Increases near [time])

    def _str_formatter_19(self, str1, _):
        '''
        19 - this is used by stats that use Blizzard's sprintf implementation
        '''
        return GameData.get_string(str1) % (self.value, )

    def _str_formatter_20(self, str1, _):
        '''
        20 - [value * -1]% [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value * -1}%'
        return self._order_by_descval(line, value)

    def _str_formatter_21(self, str1, _):
        '''
        21 - [value * -1] [string1]
        '''
        line = f'{GameData.get_string(str1)}'
        value = f'{self.value * -1}'
        return self._order_by_descval(line, value)

#    22 - [value]% [string1] [montype] (warning: this is bugged in vanilla and
#         doesn't work properly, see CE forum)
#    23 - [value]% [string1] [monster]

    def _str_formatter_24(self, str1, _):
        '''
        24 - Level {value} {skill} ({num}/{max} Charges)
        '''
        charges = self._value & 0xff
        max_charges = self._value >> 8

        level = self._param & 0x3f
        skill_data = GameData.skills[self._param >> 6]
        skill_desc = GameData.skilldesc[skill_data['skilldesc']]
        skill_name = GameData.get_string(skill_desc['str name'])

        return (f'Level {level} {skill_name}'
                f' {GameData.get_string(str1) % (charges, max_charges)}')

#    25 - not used by vanilla, present in the code but I didn't test it yet
#    26 - not used by vanilla, present in the code but I didn't test it yet

    def _str_formatter_27(self, *_):
        '''
        27 - +[value] to [skill] ([class] Only)
        '''
        skill_data = GameData.skills[self.param]
        skill_desc = GameData.skilldesc[skill_data['skilldesc']]
        skill_name = GameData.get_string(skill_desc['str name'])
        class_code = skill_data['charclass']
        class_name = GameData.playerclass_index[class_code]['Player Class']
        charstats = next(charstat for charstat in GameData.charstats
                         if charstat['class'] == class_name)
        str2 = GameData.get_string(charstats['StrClassOnly'])
        return f'{self.value:+} to {skill_name} {str2}'

#    28 - +[value] to [skill]

    # the official formatters end here, the following are helpers introduced for
    # custom skill groups that are not part of the data files but seem to be
    # hard coded in the game instead.

    def _str_formatter_30(self, str1, _):
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

    def _str_formatter_31(self, str1, _):
        '''
        poison-damage type grouping
        '''
        mindam = self.value
        maxdam = self._children[0].value
        length = self._children[1].param

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

        # fix properties with no stat assigned
        if self._code == 'dmg-max':
            self._property['stat1'] = 'maxdamage'
        if self._code == 'dmg-min':
            self._property['stat1'] = 'mindamage'

        self._itemstat = ItemStat(self._property['stat1'], param, min_value)
        for i in range(2, 8):
            if self._property[f'stat{i}']:
                self._itemstat.add_child(
                    ItemStat(self._property[f'stat{i}'], param, max_value))

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
