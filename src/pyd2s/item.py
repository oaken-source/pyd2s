'''
this module provides classes to manage individual item instances of a d2s save
'''
# I know that this file is getting a little too long, but I don't think there
# is a lot of good to gain by moving things somewhere else.
# pylint: disable=C0302

import math
import struct
import logging
from enum import Enum
from functools import total_ordering

import colorama

from pyd2s.gamedata import GameData
from pyd2s.character import CharacterClass
from pyd2s.itemstat import ItemProperty, ItemStat


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


class GemApplyType(Enum):
    '''
    an enum listing all possible gem apply types
    '''
    WEAPON = 0
    HELM = 1
    SHIELD = 2


class Item:
    '''
    save data related to a single item
    '''
    @classmethod
    def from_data(cls, buffer, offset):
        '''
        factory method for dispatching instance creation of various subclasses
        '''
        if buffer[offset:offset + 2].decode('ascii') != 'JM':
            raise ValueError('invalid save: mismatched item data header')

        # is simple?
        if buffer.getbits(offset * 8 + 37, 1):
            return SimpleItem(buffer, offset)

        # is ear?
        if buffer.getbits(offset * 8 + 32, 1):
            return EarItem(buffer, offset)

        # else it's an extended item
        return ExtendedItem(buffer, offset)

    def __init__(self, buffer, offset):
        '''
        constructor
        '''
        self._buffer = buffer
        self._offset = buffer.dynamic_offset(offset)

        self._itemdata = GameData.itemdata[self.type]

        if self._header != 'JM':
            raise ValueError('invalid save: mismatched item data header')

    @property
    def _header(self):
        '''
        produce the header of the item section - should be 'JM'
        '''
        return self._buffer[self._offset:self._offset + 2].decode('ascii')

    @property
    def type(self):
        '''
        the type of the item
        '''
        raise NotImplementedError()

    @property
    def name(self):
        '''
        the name of the item
        '''
        return GameData.get_string(self._itemdata['namestr'])

    @property
    def display_name(self):
        '''
        the name of the item as displayed by the game
        '''
        return self.name

    @property
    def is_identified(self):
        '''
        indicate whether the item is identified
        '''
        return bool(self._buffer.getbits(self._offset * 8 + 20, 1))

    @is_identified.setter
    def is_identified(self, value):
        '''
        set whether the item is identified
        '''
        self._buffer.setbits(self._offset * 8 + 20, bool(value), 1)

    @property
    def is_socketed(self):
        '''
        indicate whether the item is socketed
        '''
        return bool(self._buffer.getbits(self._offset * 8 + 27, 1))

    @property
    def is_newbie(self):
        '''
        indicate whether the item is a newbie (starter) item
        '''
        return bool(self._buffer.getbits(self._offset * 8 + 33, 1))

    @property
    def is_ethereal(self):
        '''
        indicate whether the item is ethereal
        '''
        return bool(self._buffer.getbits(self._offset * 8 + 38, 1))

    @property
    def is_personalized(self):
        '''
        indicate whether the item has been personalized by Anya
        '''
        return bool(self._buffer.getbits(self._offset * 8 + 40, 1))

    @property
    def is_runeword(self):
        '''
        indicate whether the item is a runeword
        '''
        return bool(self._buffer.getbits(self._offset * 8 + 42, 1))

    @property
    def location(self):
        '''
        the location of the item
        '''
        loc = self._buffer.getbits(self._offset * 8 + 58, 3)
        equ = self._buffer.getbits(self._offset * 8 + 61, 4)
        col = self._buffer.getbits(self._offset * 8 + 65, 4)
        row = self._buffer.getbits(self._offset * 8 + 69, 3)
        sto = self._buffer.getbits(self._offset * 8 + 73, 3)
        return (loc, equ, col, row, sto)

    @property
    def dimensions(self):
        '''
        the inventory dimensions of the item
        '''
        return {'height': self._itemdata['invheight'], 'width': self._itemdata['invwidth']}

    @property
    def quality(self):
        '''
        the item quality. This is always Normal, unless specified in extended item data
        '''
        return ItemQuality.NORMAL

    @property
    def rawdata(self):
        '''
        the raw data of the item
        '''
        return self._buffer[self._offset:self._offset + self.length]

    @property
    def length(self):
        '''
        the length of the item in bytes (to be overwritten by subclasses)
        '''
        raise NotImplementedError()


class SimpleItem(Item):
    '''
    save data related to a simple item that is not an ear
    '''
    def __init__(self, buffer, offset):
        '''
        constructor
        '''
        super().__init__(buffer, offset)

        self._properties = []
        if self._itemdata['code'] in GameData.gems:
            gem = GameData.gems[self._itemdata["code"]]

            self._properties = {
                mod_type: list(ItemStat.group_reduce(
                    ItemProperty(
                        code=gem[f'{mod_type.name.lower()}Mod{i}Code'],
                        param=int(gem[f'{mod_type.name.lower()}Mod{i}Param'] or 0),
                        min_value=int(gem[f'{mod_type.name.lower()}Mod{i}Min'] or 0),
                        max_value=int(gem[f'{mod_type.name.lower()}Mod{i}Max'] or 0),
                    ) for i in range(1, 4) if gem[f'{mod_type.name.lower()}Mod{i}Code']
                ))[::-1]
                for mod_type in GemApplyType
            }

    @property
    def type(self):
        '''
        the type of the item
        '''
        num = self._buffer.getbits(self._offset * 8 + 76, 32)
        return struct.pack('<L', num).decode('ascii').strip()

    @property
    def item_types(self):
        '''
        the list of item types of the item
        '''
        types = []
        frontier = [self._itemdata['type'], self._itemdata['type2']]

        while frontier:
            item_type, frontier = frontier[0], frontier[1:]
            if not item_type:
                continue

            types.append(item_type)
            data = GameData.itemtypes[item_type]
            frontier.extend([data['Equiv1'], data['Equiv2']])

        return types

    @property
    def num_socketed(self):
        '''
        the number of filled sockets
        '''
        return self._buffer.getbits(self._offset * 8 + 108, 3)

    @property
    def length(self):
        '''
        the length of the item in bytes
        '''
        return 14

    @property
    def required_level(self):
        '''
        the required level of this item. used for socketables like gems and runes
        '''
        return int(self._itemdata['levelreq'] or 1)

    def modifiers(self, gem_type):
        '''
        a list of modifiers applied by this item to its parent socketable
        '''
        if not isinstance(gem_type, GemApplyType):
            gem_type = GemApplyType(gem_type)
        return [prop.itemstat for prop in self._properties[gem_type]]

    def __str__(self):
        '''
        a string representation of the item
        '''
        block = [self.name]

        if 'spelldescstr' in self._itemdata and self._itemdata['spelldesc'] == '1':
            block.append(GameData.get_string(self._itemdata['spelldescstr']))

        if self._itemdata['code'] in GameData.gems:
            block.append(GameData.get_string('exinsertsockets'))

            block.append(f'\n{GameData.get_string("strgemx3")}'
                         f' {", ".join(map(str, self.modifiers(0)))}')
            block.append(f'{GameData.get_string("strgemx4")}'
                         f' {", ".join(map(str, self.modifiers(1)))}')
            block.append(f'{GameData.get_string("strgemx1")}'
                         f' {", ".join(map(str, self.modifiers(1)))}')
            block.append(f'{GameData.get_string("strgemx2")}'
                         f' {", ".join(map(str, self.modifiers(2)))}')

        if self.required_level > 1:
            block.append(f'\nRequired Level: {self.required_level}')

        return '\n'.join(block)


class EarItem(Item):
    '''
    save data related to an ear
    '''
    def __init__(self, buffer, offset):
        '''
        constructor
        '''
        super().__init__(buffer, offset)
        self._length = math.ceil((86 + (len(self.character_name) + 1) * 7) / 8)

    @property
    def name(self):
        '''
        a base name of the item
        '''
        return f"{self.character_name}'s Ear"

    @property
    def type(self):
        '''
        the type of the item
        '''
        return 'ear'

    @property
    def display_name(self):
        '''
        this item is always displayed with its base name
        '''
        return self.name

    @property
    def character_class(self):
        '''
        the character class of the ear
        '''
        return CharacterClass(self._buffer.getbits(self._offset * 8 + 76, 3))

    @property
    def character_level(self):
        '''
        the character level of the ear
        '''
        return self._buffer.getbits(self._offset * 8 + 79, 3)

    @property
    def character_name(self):
        '''
        the name of the character who used to own this ear
        '''
        ptr = self._buffer.bit_pointer(self._offset * 8 + 86)
        return ptr.read_string()

    @property
    def length(self):
        '''
        the length of the item in bytes
        '''
        return self._length

    def __str__(self):
        '''
        a string representation of the item
        '''
        block = [self.name]

        block.append(f'{self.character_class}')
        block.append(f'Level {self.character_level}')

        return '\n'.join(block)


class ExtendedItem(SimpleItem):
    '''
    save data related to an extended item
    '''
    def __init__(self, buffer, offset):
        # it makes little sense to split this method up, it's most concise this way
        # pylint: disable=R0912, R0915
        '''
        constructor
        '''
        super().__init__(buffer, offset)

        self._attributes = {}

        ptr = buffer.bit_pointer(self._offset * 8 + 154)

        # icon select
        if ptr.read(1):
            self._attributes['icon_id'] = ptr.read(3)

        # class item affix
        if ptr.read(1):
            self._attributes['class_affix'] = ptr.read(11)

        # low quality details
        if self.quality == ItemQuality.LOW_QUALITY:
            self._attributes['lq_affix'] = ptr.read(3)

        # high quality details
        if self.quality == ItemQuality.HIGH_QUALITY:
            self._attributes['hq_affix'] = ptr.read(3)

        # magic item details
        if self.quality == ItemQuality.MAGICAL:
            self._attributes['magic_prefix'] = ptr.read(11)
            self._attributes['magic_suffix'] = ptr.read(11)

        # set item details part 1
        if self.quality == ItemQuality.SET:
            self._attributes['set_id'] = ptr.read(12)

        # rare item details
        if self.quality == ItemQuality.RARE:
            self._attributes['rare_name_1'] = ptr.read(8)
            self._attributes['rare_name_2'] = ptr.read(8)

            for i in range(1, 4):
                if ptr.read(1):
                    self._attributes[f'rare_prefix_{i}'] = ptr.read(11)
                if ptr.read(1):
                    self._attributes[f'rare_suffix_{i}'] = ptr.read(11)

        # unique item details
        if self.quality == ItemQuality.UNIQUE:
            self._attributes['unique_id'] = ptr.read(12)

        # crafted item details
        if self.quality == ItemQuality.CRAFTED:
            self._attributes['crafted_name_1'] = ptr.read(8)
            self._attributes['crafted_name_2'] = ptr.read(8)

            for i in range(1, 4):
                if ptr.read(1):
                    self._attributes[f'crafted_prefix_{i}'] = ptr.read(11)
                if ptr.read(1):
                    self._attributes[f'crafted_suffix_{i}'] = ptr.read(11)

        # rune word details
        if self.is_runeword:
            self._attributes['runeword_id'] = ptr.read(12)
            ptr.read(4)

        # personalization details
        if self.is_personalized:
            self._attributes['personalized_name'] = ptr.read_string()

        # tomes
        if self._itemdata['type'] == 'book':
            ptr.read(5)

        # skip one unknown bit
        ptr.read(1)

        # armor details
        if self._itemdata['kind'] == 'armor':
            self._attributes['defense'] = ptr.read(11) - 10

        # durability
        if self._itemdata['kind'] in ['armor', 'weapons']:
            max_durability = ptr.read(8)
            if max_durability > 0:
                self._attributes['max_durability'] = max_durability
                self._attributes['durability'] = ptr.read(8)
                ptr.read(1)

        # stackables
        if self._itemdata.get('stackable', 0) == '1':
            self._attributes['quantity'] = ptr.read(9)

        # socketed items
        if self.is_socketed:
            self._attributes['socket_count'] = ptr.read(4)

        # set details part 2
        if self.quality == ItemQuality.SET:
            set_properties = ptr.read(5)

        # the first attribute list are regular affixes and modifiers
        self._attributes['enhancements'] = ItemStat.read_list(ptr)

        # set items have one or two extra modifier lists
        if self.quality == ItemQuality.SET:
            if set_properties >= 1:
                self._attributes['set_enhancements_1'] = ItemStat.read_list(ptr)
            if set_properties >= 3:
                self._attributes['set_enhancements_3'] = ItemStat.read_list(ptr)

        # rune words have their own modifier list
        if self.is_runeword:
            self._attributes['enhancements'].extend(ItemStat.read_list(ptr))

        # round the item length up to the nearest byte
        length = (ptr.distance + 154 - 1) // 8 + 1

        # handle items placed in sockets
        self._socketed = []
        start = offset + length
        gemapplytype = int(self._itemdata['gemapplytype'] or 0)
        for i in range(self.num_socketed):
            item = Item.from_data(self._buffer, start)
            start += item.length
            length += item.length
            self._socketed.append(item)
            self._attributes['enhancements'].extend(item.modifiers(gemapplytype))

        self._attributes['enhancements'].sort(reverse=True)

        # mark the length of the item in bytes
        self._length = length

    @property
    def required_level(self):
        '''
        produce the required level of the item
        '''
        # base required level
        res = int(self._itemdata['levelreq'] or 1)

        # magic and rare prefix required levels
        for key in ['magic_prefix', *[f'rare_prefix_{i}' for i in range(1, 4)]]:
            prefix = int(self._attributes.get(key, 0))
            if prefix:
                res = max(res, int(GameData.magicprefix[prefix]['levelreq']))
        for key in ['magic_suffix', *[f'rare_suffix_{i}' for i in range(1, 4)]]:
            suffix = int(self._attributes.get(key, 0))
            if suffix:
                res = max(res, int(GameData.magicsuffix[suffix]['levelreq']))

        # to-skill modifiers required levels
        mods = [
            enhancement for enhancement in self._attributes['enhancements']
            if enhancement.stat == 'item_singleskill']
        for mod in mods:
            skill_data = GameData.skills[mod.param]
            res = max(res, int(skill_data['reqlevel'] or 1))

        # set item required level
        if 'set_id' in self._attributes:
            set_data = GameData.setitems[int(self._attributes['set_id'])]
            res = max(res, int(set_data['lvl req'] or 1))

        # unique item required level
        if 'unique_id' in self._attributes and self._attributes['unique_id'] != 0xfff:
            unique_data = GameData.uniqueitems[self._attributes['unique_id']]
            res = max(res, int(unique_data['lvl req']))

        # socketables required levels
        for item in self._socketed:
            res = max(res, item.required_level)

        return res

    @property
    def extended_name(self):
        '''
        a full name of the item with affixes always shown
        '''
        name = self.name

        # different names by item quality
        if self.quality == ItemQuality.LOW_QUALITY:
            prefix = GameData.lowqualityitems[self._attributes['lq_affix']]['Name']
            name = f'{prefix} {name}'
        if self.quality == ItemQuality.HIGH_QUALITY:
            name = f'Superior {name}'
        if self.quality == ItemQuality.MAGICAL:
            if self._attributes['magic_prefix']:
                affix = GameData.magicprefix[self._attributes['magic_prefix']]
                name = f'{GameData.get_string(affix["Name"])} {name}'
            if self._attributes['magic_suffix']:
                affix = GameData.magicsuffix[self._attributes['magic_suffix']]
                name = f'{name} {GameData.get_string(affix["Name"])}'
        if self.quality == ItemQuality.SET:
            name = GameData.get_string(
                GameData.setitems[self._attributes['set_id']]['index'])
        if self.quality in [ItemQuality.RARE, ItemQuality.CRAFTED]:
            name_1 = GameData.get_string(
                GameData.rareaffix[self._attributes['rare_name_1']]['name'])
            name_2 = GameData.get_string(
                GameData.rareaffix[self._attributes['rare_name_2']]['name'])
            name = f'{name_1} {name_2}'
        if self.quality == ItemQuality.UNIQUE:
            if self._attributes['unique_id'] != 0xfff:
                unique_item = GameData.uniqueitems[self._attributes['unique_id']]
                logging.debug(unique_item)
                name = GameData.get_string(unique_item['index'])

        # runewords are treated differently
        if self.is_runeword:
            runes = [item.type for item in self._socketed] + [''] * (6 - len(self._socketed))
            runeword = next(rune for rune in GameData.runes.values() if all(
                rune[f'Rune{i + 1}'] == runes[i] for i in range(6)))
            name = GameData.get_string(runeword['Name'])

        # gemmed, but no runeword gets a prefix
        if self.num_socketed and not self.is_runeword:
            name = f'Gemmed {name}'

        return name

    @property
    def display_name(self):
        '''
        the name of the item, with affixes hidden if unidentified
        '''
        if self.quality >= ItemQuality.MAGICAL and not self.is_identified:
            return self.name
        return self.extended_name

    @property
    def name_color(self):
        '''
        the color of the item name
        '''
        # R0911 complains for too many return statements here, but it should still be okay
        # it might make sense to encode the item color in the ItemQuality Enum though.
        # pylint: disable=R0911

        if self.is_runeword:
            return colorama.Fore.YELLOW + colorama.Style.DIM

        # determine color by item quality
        if self.quality == ItemQuality.MAGICAL:
            return colorama.Fore.BLUE
        if self.quality == ItemQuality.SET:
            return colorama.Fore.GREEN
        if self.quality == ItemQuality.RARE:
            return colorama.Fore.YELLOW
        if self.quality == ItemQuality.UNIQUE:
            return colorama.Fore.YELLOW + colorama.Style.DIM
        if self.quality == ItemQuality.CRAFTED:
            return colorama.Fore.RED + colorama.Style.DIM

        # otherwise, check for sockets / ethereal
        if self.is_socketed or self.is_ethereal:
            return colorama.Fore.LIGHTBLACK_EX

        return colorama.Fore.WHITE

    @property
    def uid(self):
        '''
        the unique id of the item
        '''
        return self._buffer.getbits(self._offset * 8 + 111, 32)

    @property
    def ilvl(self):
        '''
        the item level
        '''
        return self._buffer.getbits(self._offset * 8 + 143, 7)

    @property
    def quality(self):
        '''
        the item quality
        '''
        return ItemQuality(self._buffer.getbits(self._offset * 8 + 150, 4))

    @property
    def length(self):
        '''
        the length of the item in bytes
        '''
        return self._length

    def _apply_mods(self, value, stat):
        '''
        apply the modifiers to the given stat
        '''
        mods = [mod for mod in self._attributes['enhancements'] if stat in mod.applies_to]
        bonus = sum(mod.apply_to(value) for mod in mods)
        return value + bonus

    def _str_block_header(self):
        '''
        the header of the item string, includes:
            - the item name
            - the item subname, if any
            - rune letters, if any
            - charm and socketables messages
        '''
        # start with the colored item name
        block = [f'{self.name_color}{self.display_name}{colorama.Style.RESET_ALL}']

        # if the item is rare, set, unique or crafted add a the base name in the name color
        # unless SkipName is set, or the unique id is 0xFFF
        if (self.quality > ItemQuality.MAGICAL and self.is_identified
                and not int(self._itemdata['SkipName'] or 0)
                and not self._attributes.get('unique_id', 0) == 0xfff):
            block.append(f'{self.name_color}{self.name}{colorama.Style.RESET_ALL}')

        # if the item is a runeword, add the base name in grey
        if self.is_runeword:
            block.append(f'{colorama.Fore.LIGHTBLACK_EX}{self.name}{colorama.Fore.RESET}')

        # if the item has runes socketed show the rune letters
        if self._socketed:
            runes = [GameData.gems[item.type]['letter'] for item in self._socketed]
            block.append(f"{colorama.Fore.YELLOW}{colorama.Style.DIM}"
                         f"'{''.join(runes)}'{colorama.Style.RESET_ALL}")

        # add the charm line
        if GameData.itemtypes[self._itemdata['type']]['Equiv1'] == 'char':
            block.append(GameData.get_string('charmdes'))

        # add the socketables line for jewels
        if self._itemdata['code'] == 'jew':
            block.append(GameData.get_string('exinsertsocketsx'))

        return block

    def _str_block_armor(self):
        '''
        the armor details block of the item string, includes:
            - the defense, if any (blue if magically enhanced)
            - the block chance, if this is a shield
        '''
        block = []

        # handle defense, if recorded in the attributes
        if 'defense' in self._attributes:
            defense = self._attributes['defense']
            new_defense = self._apply_mods(defense, 'armorclass')

            line = GameData.get_string('itemstats1h')
            if self.is_identified and new_defense != defense:
                line += f' {colorama.Fore.BLUE}{new_defense}{colorama.Fore.RESET}'
            else:
                line += f' {defense}'
            block.append(line)

        # handle block for shields
        if 'shld' in self.item_types:
            # this calculation does not include the class bonus to block chance
            chance = int(self._itemdata['block']) + 20
            new_chance = self._apply_mods(chance, 'toblock')

            line = GameData.get_string('itemstats1r')
            if self.is_identified:
                line += f'{colorama.Fore.BLUE}{new_chance}%{colorama.Fore.RESET}'
            else:
                line += f'{colorama.Fore.BLUE}{chance}%{colorama.Fore.RESET}'
            block.append(line)

        return block

    def _str_block_damage_single(self, key_dam, str1, key_stat):
        '''
        one line of damage data for a given damage type
        '''
        if key_dam % 'min' not in self._itemdata or not int(self._itemdata[key_dam % 'min'] or 0):
            return []

        mindam = int(self._itemdata[key_dam % 'min'])
        maxdam = int(self._itemdata[key_dam % 'max'])

        if self.quality == ItemQuality.LOW_QUALITY:
            mindam = mindam * 75 // 100
            maxdam = maxdam * 75 // 100
        if self.is_ethereal:
            mindam = mindam * 3 // 2
            maxdam = maxdam * 3 // 2

        new_mindam = self._apply_mods(mindam, key_stat % 'min')
        new_maxdam = self._apply_mods(maxdam, key_stat % 'max')

        new_maxdam = max(new_maxdam, new_mindam + 1)

        line = GameData.get_string(str1)
        if self.is_identified and (mindam != new_mindam or maxdam != new_maxdam):
            line += (f' {colorama.Fore.BLUE}{new_mindam} to '
                     f'{new_maxdam}{colorama.Fore.RESET}')
        else:
            line += f' {mindam} to {maxdam}'

        return [line]

    def _str_block_damage(self):
        '''
        the weapon damage details block of the item string, includes:
            - the throw damage, if any (blue if magically enhanced)
            - the one-hand damage, if any (blue if magically enhanced)
            - the two-hand damage, if any (blue if magically enhanced)
        '''
        block = []

        # first throw damage
        block.extend(self._str_block_damage_single(
            '%smisdam', 'itemstats1n', 'item_throw_%sdamage'))
        # second one-handed damage
        block.extend(self._str_block_damage_single(
            '%sdam', 'itemstats1l', '%sdamage'))
        # third two-handed damage
        block.extend(self._str_block_damage_single(
            '2hand%sdam', 'itemstats1m', 'secondary_%sdamage'))

        return block

    def _str_block_attack_speed(self):
        '''
        attack speed details. this is displayed numerically instead of the labels in-game
        since the attack speed varies depending on class bonuses. so little point.
        '''
        if 'weap' not in self.item_types:
            return []

        # this could probably be handled better. but how?
        weapon_classes = {
            'mace': 'mace',
            'club': 'mace',
            'hamm': 'mace',
            'scep': 'mace',
            'axe': 'axe',
            'taxe': 'axe',
            'swor': 'sword',
            'knif': 'dagger',
            'tkni': 'dagger',
            'ajav': 'javelin',
            'jave': 'javelin',
            'aspe': 'spear',
            'spea': 'spear',
            'abow': 'bow',
            'bow': 'bow',
            'orb': 'staff',
            'staf': 'staff',
            'wand': 'staff',
            'pole': 'polearm',
            'xbow': 'crossbow',
            'h2h': 'h2h',
            'h2h2': 'h2h',
        }

        weapon_class = GameData.get_string(
            f'weapondesc{weapon_classes[self._itemdata["type"]]}')
        speed = int(self._itemdata['speed'] or 0)
        return [f'{weapon_class} - [{speed}] Attack Speed']

    def _str_block_durability(self):
        '''
        durability and quantity information about the item, includes:
            - durability and max durability, if any and not stacked
            - quantity if any
        '''
        block = []

        # handle quantity
        if 'quantity' in self._attributes:
            block.append(f'Quantity: {self._attributes["quantity"]}')

        # handle durability
        elif ('durability' in self._attributes
              and not int(self._itemdata['nodurability'] or 0)):
            durability = self._attributes['durability']
            max_durability = self._attributes['max_durability']

            new_max_durability = self._apply_mods(max_durability, 'maxdurability')

            line = GameData.get_string('itemstats1d')
            line += f' {durability} of {new_max_durability}'

            block.append(line)

        return block

    def _str_block_requirements(self):
        '''
        requirements information about the item, includes:
            - required class, if any
            - required strength, if any
            - required dexterity, if any
            - required level, if any
        '''
        block = []

        # handle class requirement
        if 'type' in self._itemdata and self._itemdata['type']:
            item_class = GameData.itemtypes[self._itemdata['type']]
            if item_class['Class']:
                block.append(
                    f'{colorama.Fore.RED}'
                    f'({GameData.get_string("partychar" + item_class["Class"])} Only)'
                    f'{colorama.Fore.RESET}')

        # handle str / dex requirement
        for (req, str1) in [('reqdex', 'itemstats1f'), ('reqstr', 'itemstats1e')]:
            if req in self._itemdata and int(self._itemdata[req] or 0):
                value = int(self._itemdata[req])
                if self.is_ethereal:
                    value -= 10
                if value > 0:
                    block.append(f'{GameData.get_string(str1)} {value}')

        # handle level requirement
        if self.required_level > 1 and self.is_identified:
            block.append(f'{GameData.get_string("itemstats1p")} {self.required_level}')

        return block

    def _str_block_magic_mods(self):
        '''
        the magic modifiers list of the item, includes:
            - any mods added by magic / rare / set affixes
            - +50% dmg to undead for blunt weapons
            - ethereal
            - sockets
        '''
        block = []

        # handle magical properties
        if self.quality.value >= ItemQuality.MAGICAL.value and not self.is_identified:
            block.append(f'{colorama.Fore.RED}Unidentified{colorama.Fore.RESET}')
        elif 'enhancements' in self._attributes:
            for enhancement in self._attributes['enhancements']:
                if enhancement.is_visible:
                    block.append(f'{colorama.Fore.BLUE}{enhancement}{colorama.Fore.RESET}')

        # handle blunt weapons
        if 'blun' in self.item_types:
            block.append(f'{colorama.Fore.BLUE}+50% Damage to Undead{colorama.Fore.RESET}')

        # handle ethereal items
        line = []
        if self.is_ethereal:
            line.append(
                f'{colorama.Fore.BLUE}Ethereal (Cannot be Repaired){colorama.Fore.RESET}')

        # handle sockets
        if self.is_socketed:
            line.append(
                f'{colorama.Fore.BLUE}Socketed '
                f'({self._attributes["socket_count"]}){colorama.Fore.RESET}')

        if line:
            block.append(', '.join(line))

        return block

    def _str_block_set_list(self):
        '''
        the set list of the item, includes:
            - the name of the set
            - all members of the set
        '''
        block = []

        # handle set lists
        if self.quality == ItemQuality.SET:
            set_name = GameData.setitems[int(self._attributes['set_id'])]['set']
            block.append(f'\n{colorama.Fore.YELLOW}{colorama.Style.DIM}'
                         f'{GameData.get_string(set_name)}'
                         f'{colorama.Style.RESET_ALL}')

            for set_item in reversed(
                    [item for item in GameData.setitems if item['set'] == set_name]):
                block.append(f'{colorama.Fore.GREEN}'
                             f'{GameData.get_string(set_item["index"])}'
                             f'{colorama.Fore.RESET}')

        return block

    def __str__(self):
        '''
        a string representation of the item
        '''
        # start with the header
        block = self._str_block_header()

        # followed by armor properties
        block.extend(self._str_block_armor())

        # followed by damage properties
        block.extend(self._str_block_damage())

        # followed by attack speed, if this a set item (mad, I know.)
        if self.quality == ItemQuality.SET:
            block.extend(self._str_block_attack_speed())

        # followed by quantity and durability
        block.extend(self._str_block_durability())

        # followed by requirements
        block.extend(self._str_block_requirements())

        # followed by attack speed, if this is not a set item
        if self.quality != ItemQuality.SET:
            block.extend(self._str_block_attack_speed())

        # followed by magic modifiers
        block.extend(self._str_block_magic_mods())

        # followed by set details
        block.extend(self._str_block_set_list())

        # and done.
        return '\n'.join(block)
