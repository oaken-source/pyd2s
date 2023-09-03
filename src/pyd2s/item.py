'''
this module provides classes to manage individual item instances of a d2s save
'''

import math
import struct
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
        self._offset = offset

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
    @property
    def type(self):
        '''
        the type of the item
        '''
        num = self._buffer.getbits(self._offset * 8 + 76, 32)
        return struct.pack('<L', num).decode('ascii').strip()

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

    def __str__(self):
        '''
        a string representation of the item
        '''
        block = [self.name]

        if 'spelldescstr' in self._itemdata and self._itemdata['spelldesc'] == '1':
            block.append(GameData.get_string(self._itemdata['spelldescstr']))

        if self._itemdata['code'] in GameData.gems:
            block.append('Can be Inserted into Socketed Items')

            gem = GameData.gems[self._itemdata["code"]]

            def group_reduce(iterable):
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

            props = {
                mod_type: list(group_reduce(
                    ItemProperty(
                        code=gem[f'{mod_type}Mod{i}Code'],
                        param=int(gem[f'{mod_type}Mod{i}Param'] or 0),
                        min_value=int(gem[f'{mod_type}Mod{i}Min'] or 0),
                        max_value=int(gem[f'{mod_type}Mod{i}Max'] or 0),
                    ) for i in range(1, 4) if gem[f'{mod_type}Mod{i}Code']
                ))[::-1]
                for mod_type in ['weapon', 'helm', 'shield']
            }

            block.append(f'\nWeapons: {", ".join(map(str, props["weapon"]))}')
            block.append(f'Armor: {", ".join(map(str, props["helm"]))}')
            block.append(f'Helms: {", ".join(map(str, props["helm"]))}')
            block.append(f'Shields: {", ".join(map(str, props["shield"]))}')

        if int(self._itemdata['levelreq'] or 0) > 1:
            block.append(f'\nRequired Level: {self._itemdata["levelreq"]}')

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
        name = ""
        pos = 86
        while True:
            next_char = self._buffer.getbits(self._offset * 8 + pos, 7)
            pos += 7
            if next_char == 0:
                break
            name += chr(next_char)
        return name

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
        '''
        constructor
        '''
        super().__init__(buffer, offset)

        # parse extended data
        self._attributes = {}
        self._immediate_mods = {}
        pos = 154

        self._levelreq = int(self._itemdata['levelreq'] or 1)

        # icon select
        if self._buffer.getbits(self._offset * 8 + pos, 1):
            self._attributes['icon_id'] = self._buffer.getbits(self._offset * 8 + pos + 1, 3)
            pos += 4
        else:
            pos += 1

        # class item affix
        if self._buffer.getbits(self._offset * 8 + pos, 1):
            self._attributes['class_affix'] = self._buffer.getbits(self._offset * 8 + pos + 1, 11)
            pos += 12
        else:
            pos += 1

        # low quality details
        if self.quality == ItemQuality.LOW_QUALITY:
            self._attributes['lq_name_prefix'] = self._buffer.getbits(self._offset * 8 + pos, 3)
            pos += 3

        # high quality details
        if self.quality == ItemQuality.HIGH_QUALITY:
            self._attributes['hq_name_prefix'] = self._buffer.getbits(self._offset * 8 + pos, 3)
            pos += 3

        # magic item details
        if self.quality == ItemQuality.MAGICAL:
            affix = self._buffer.getbits(self._offset * 8 + pos, 11)
            pos += 11
            self._attributes['magic_prefix'] = affix
            if affix:
                affix_info = GameData.magicprefix[affix]
                if affix_info['levelreq']:
                    self._levelreq = max(self._levelreq, int(affix_info['levelreq']))
            affix = self._buffer.getbits(self._offset * 8 + pos, 11)
            pos += 11
            self._attributes['magic_suffix'] = affix
            if affix:
                affix_info = GameData.magicsuffix[affix]
                if affix_info['levelreq']:
                    self._levelreq = max(self._levelreq, int(affix_info['levelreq']))

        # set item details part 1
        if self.quality == ItemQuality.SET:
            self._attributes['set_id'] = self._buffer.getbits(self._offset * 8 + pos, 12)
            pos += 12

        # rare item details
        if self.quality == ItemQuality.RARE:
            self._attributes['rare_name_1'] = self._buffer.getbits(self._offset * 8 + pos, 8)
            pos += 8
            self._attributes['rare_name_2'] = self._buffer.getbits(self._offset * 8 + pos, 8)
            pos += 8
            for i in range(1, 4):
                if self._buffer.getbits(self._offset * 8 + pos, 1):
                    affix = self._buffer.getbits(self._offset * 8 + pos + 1, 11)
                    self._attributes[f'rare_prefix_{i}'] = affix
                    affix_info = GameData.magicprefix[affix]
                    if affix_info['levelreq']:
                        self._levelreq = max(self._levelreq, int(affix_info['levelreq']))
                    pos += 12
                else:
                    pos += 1
                if self._buffer.getbits(self._offset * 8 + pos, 1):
                    affix = self._buffer.getbits(self._offset * 8 + pos + 1, 11)
                    self._attributes[f'rare_suffix_{i}'] = affix
                    affix_info = GameData.magicsuffix[affix]
                    if affix_info['levelreq']:
                        self._levelreq = max(self._levelreq, int(affix_info['levelreq']))
                    pos += 12
                else:
                    pos += 1

        # unique item details
        if self.quality == ItemQuality.UNIQUE:
            self._attributes['unique_id'] = self._buffer.getbits(self._offset * 8 + pos, 12)
            pos += 12

        # crafted item details
        if self.quality == ItemQuality.CRAFTED:
            self._attributes['crafted_name_1'] = self._buffer.getbits(self._offset * 8 + pos, 8)
            pos += 8
            self._attributes['crafted_name_2'] = self._buffer.getbits(self._offset * 8 + pos, 8)
            pos += 8
            for i in range(1, 4):
                if self._buffer.getbits(self._offset * 8 + pos, 1):
                    self._attributes[f'crafted_prefix_{i}'] = \
                        self._buffer.getbits(self._offset * 8 + pos + 1, 11)
                    pos += 12
                else:
                    pos += 1
                if self._buffer.getbits(self._offset * 8 + pos, 1):
                    self._attributes[f'crafted_suffix_{i}'] = \
                        self._buffer.getbits(self._offset * 8 + pos + 1, 11)
                    pos += 12
                else:
                    pos += 1

        # rune word details
        if self.is_runeword:
            self._attributes['runeword_id'] = self._buffer.getbits(self._offset * 8 + pos, 12)
            pos += 12 + 4

        # personalization details
        if self.is_personalized:
            name = ''
            while True:
                next_char = self._buffer.getbits(self._offset * 8 + pos, 7)
                pos += 7
                if next_char == 0:
                    break
                name += chr(next_char)
            self._attributes['personalized_name'] = name

        # tomes
        if self._itemdata['type'] == 'book':
            pos += 5

        # skip one unknown bit
        pos += 1

        # armor details
        if self._itemdata['kind'] == 'armor':
            self._attributes['defense'] = self._buffer.getbits(self._offset * 8 + pos, 11) - 10
            pos += 11

        # durability
        if self._itemdata['kind'] in ['armor', 'weapons']:
            self._attributes['max_durability'] = self._buffer.getbits(self._offset * 8 + pos, 8)
            pos += 8
            if self._attributes['max_durability'] > 0:
                self._attributes['durability'] = self._buffer.getbits(self._offset * 8 + pos, 8)
                pos += 8
                pos += 1
            else:
                self._attributes['durability'] = 0

        # stackables
        if 'stackable' in self._itemdata and self._itemdata['stackable'] == '1':
            self._attributes['quantity'] = self._buffer.getbits(self._offset * 8 + pos, 9)
            pos += 9

        # socketed items
        if self.is_socketed:
            self._attributes['socket_count'] = self._buffer.getbits(self._offset * 8 + pos, 4)
            pos += 4

        # set details part 2
        if self.quality == ItemQuality.SET:
            # set_properties = self._buffer.getbits(self._offset * 8 + pos, 5)
            pos += 5

        def group_reduce(iterable):
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

        # enhancements
        enhancements = []
        while True:
            eid = self._buffer.getbits(self._offset * 8 + pos, 9)
            pos += 9
            if eid == 0x1FF:
                break

            consecutive = GameData.get_consecutive_item_stat_blocks(eid)
            group = []
            for _eid in range(eid, eid + consecutive):
                item_stat_cost = GameData.itemstatcost[_eid]
                value = 0
                param = 0
                if item_stat_cost['Save Param Bits'] and int(item_stat_cost['Save Param Bits']):
                    field_width = int(item_stat_cost['Save Param Bits'])
                    param = self._buffer.getbits(self._offset * 8 + pos, field_width)
                    pos += field_width
                if item_stat_cost['Save Bits'] and int(item_stat_cost['Save Bits']):
                    field_width = int(item_stat_cost['Save Bits'])
                    value = self._buffer.getbits(self._offset * 8 + pos, field_width)
                    if item_stat_cost['Save Add'] and int(item_stat_cost['Save Add']):
                        value -= int(item_stat_cost['Save Add'])
                    pos += field_width
                group.append(ItemStat(_eid, param, value))

            for child in group[1:]:
                group[0].add_child(child)

            enhancements.append(group[0])

        enhancements = group_reduce(enhancements)
        enhancements.sort(reverse=True)
        self._attributes['enhancements'] = enhancements

        if self.quality == ItemQuality.SET:
            set_enhancements = []
            while True:
                eid = self._buffer.getbits(self._offset * 8 + pos, 9)
                pos += 9
                if eid == 0x1FF:
                    break

                consecutive = GameData.get_consecutive_item_stat_blocks(eid)
                group = []
                for _eid in range(eid, eid + consecutive):
                    item_stat_cost = GameData.itemstatcost[_eid]
                    value = 0
                    param = 0
                    if item_stat_cost['Save Param Bits'] and int(item_stat_cost['Save Param Bits']):
                        field_width = int(item_stat_cost['Save Param Bits'])
                        param = self._buffer.getbits(self._offset * 8 + pos, field_width)
                        pos += field_width
                    if item_stat_cost['Save Bits'] and int(item_stat_cost['Save Bits']):
                        field_width = int(item_stat_cost['Save Bits'])
                        value = self._buffer.getbits(self._offset * 8 + pos, field_width)
                        if item_stat_cost['Save Add'] and int(item_stat_cost['Save Add']):
                            value -= int(item_stat_cost['Save Add'])
                        pos += field_width
                    group.append(ItemStat(_eid, param, value))

                for child in group[1:]:
                    group[0].add_child(child)

                set_enhancements.append(group[0])

            set_enhancements.sort(reverse=True)
            self._attributes['set_enhancements'] = set_enhancements

        # mark the length of the item in bits
        self._length = pos

    @property
    def extended_name(self):
        '''
        a full name of the item with affixes always shown
        '''
        name = self.name

        if self.quality == ItemQuality.LOW_QUALITY:
            prefix = GameData.lowqualityitems[self._attributes['lq_name_prefix']]['Name']
            name = f'{prefix} {name}'
        if self.quality == ItemQuality.HIGH_QUALITY:
            name = f'Superior {name}'
        if self.quality == ItemQuality.MAGICAL:
            if self._attributes['magic_prefix']:
                affix = GameData.magicprefix[self._attributes["magic_prefix"]]
                name = f'{GameData.get_string(affix["Name"])} {name}'
            if self._attributes['magic_suffix']:
                affix = GameData.magicsuffix[self._attributes["magic_suffix"]]
                name = f'{name} {GameData.get_string(affix["Name"])}'
        if self.quality == ItemQuality.SET:
            raise NotImplementedError()
        if self.quality == ItemQuality.RARE:
            name_1 = GameData.get_string(
                GameData.rareaffix[self._attributes['rare_name_1']]['name'])
            name_2 = GameData.get_string(
                GameData.rareaffix[self._attributes['rare_name_2']]['name'])
            name = f'{name_1} {name_2}'
        if self.quality == ItemQuality.UNIQUE:
            raise NotImplementedError()
        if self.quality == ItemQuality.CRAFTED:
            raise NotImplementedError()

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
        if self.quality == ItemQuality.MAGICAL:
            return colorama.Fore.BLUE
        if self.quality == ItemQuality.SET:
            return colorama.Fore.GREEN
        if self.quality == ItemQuality.RARE:
            return colorama.Fore.YELLOW
        if self.quality == ItemQuality.UNIQUE:
            raise NotImplementedError()
        if self.quality == ItemQuality.CRAFTED:
            raise NotImplementedError()

        # only normal / hq / lq items are left, check for sockets / ethereal
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
        return math.ceil(self._length / 8)

    def __str__(self):
        '''
        a string representation of the item
        '''
        name = self.display_name
        if self.quality > ItemQuality.MAGICAL and self.is_identified:
            name += f'\n{self.name}'
        name = f'{self.name_color}{name}{colorama.Fore.RESET}'

        block = [name]

        # handle charms
        if GameData.itemtypes[self._itemdata['type']]['Equiv1'] == 'char':
            block.append('Keep in Inventory to Gain Bonus')

        # handle socketables
        if self._itemdata['code'] == 'jew':
            block.append('Can be Inserted into Socketed Items')

        # handle defense
        if 'defense' in self._attributes:
            defense = self._attributes['defense']
            new_defense = defense
            mods = [
                enhancement for enhancement in self._attributes['enhancements']
                if enhancement.stat == 'item_armor_percent']
            if mods and self.is_identified:
                new_defense = (defense * (100 + mods[0].value)) // 100
            if new_defense > defense:
                block.append(f'Defense: {colorama.Fore.BLUE}{new_defense}{colorama.Fore.RESET}')
            else:
                block.append(f'Defense: {defense}')

        # handle block
        if self._itemdata['type'] in ['shie', 'head']:
            # excluding character-specific bonus to block chance
            chance = int(self._itemdata['block']) + 20
            mods = [
                enhancement for enhancement in self._attributes['enhancements']
                if enhancement.stat == 'toblock']
            if mods and self.is_identified:
                chance += int(mods[0].value)
            block.append(f'Chance to Block: {colorama.Fore.BLUE}{chance}%{colorama.Fore.RESET}')

        # handle damage
        if 'minmisdam' in self._itemdata and int(self._itemdata['minmisdam'] or 0):
            block.append(
                'Throw Damage: '
                f'{self._itemdata["minmisdam"]} to {self._itemdata["maxmisdam"]}')

        if 'mindam' in self._itemdata and int(self._itemdata['mindam'] or 0):
            mindam = int(self._itemdata['mindam'])
            new_mindam = mindam
            maxdam = int(self._itemdata['maxdam'])
            new_maxdam = maxdam
            mods = [
                enhancement for enhancement in self._attributes['enhancements']
                if enhancement.stat == 'item_maxdamage_percent']
            if mods and self.is_identified:
                new_mindam = (mindam * (100 + mods[0].value)) // 100
                new_maxdam = (maxdam * (100 + mods[0].value)) // 100
            mods = [
                enhancement for enhancement in self._attributes['enhancements']
                if enhancement.stat == 'maxdamage']
            if mods and self.is_identified:
                new_maxdam = new_maxdam + mods[0].value
            mods = [
                enhancement for enhancement in self._attributes['enhancements']
                if enhancement.stat == 'mindamage']
            if mods and self.is_identified:
                new_mindam = new_mindam + mods[0].value
            if new_maxdam > maxdam or new_mindam > mindam:
                block.append(
                    'One-Hand Damage: '
                    f'{colorama.Fore.BLUE}{mindam} to {new_maxdam}{colorama.Fore.RESET}')
            else:
                block.append(f'One-Hand Damage: {mindam} to {maxdam}')

        if '2handmindam' in self._itemdata and int(self._itemdata['2handmindam'] or 0):
            block.append(
                'Two-Hand Damage: '
                f'{self._itemdata["2handmindam"]} to {self._itemdata["2handmaxdam"]}')

        # handle quantity
        if 'quantity' in self._attributes:
            block.append(f'Quantity: {self._attributes["quantity"]}')

        # handle durability
        elif 'durability' in self._attributes:
            durability = self._attributes['durability']
            max_durability = self._attributes['max_durability']
            new_max_durability = max_durability
            mods = [
                enhancement for enhancement in self._attributes['enhancements']
                if enhancement.stat == 'item_maxdurability_percent']
            if mods and self.is_identified:
                new_max_durability = (max_durability * (100 + mods[0].value)) // 100
            block.append(f'Durability: {durability} of {new_max_durability}')

        # handle class requirement
        if 'type' in self._itemdata and self._itemdata['type']:
            item_class = GameData.itemtypes[self._itemdata['type']]
            if item_class['Class']:
                block.append(
                    f'{colorama.Fore.RED}'
                    f'({GameData.get_string("partychar" + item_class["Class"])} Only)'
                    f'{colorama.Fore.RESET}')

        # handle dex requirement
        if 'reqdex' in self._itemdata and int(self._itemdata['reqdex'] or 0):
            block.append(f'Required Dexterity: {self._itemdata["reqdex"]}')

        # handle str requirement
        if 'reqstr' in self._itemdata and int(self._itemdata['reqstr'] or 0):
            block.append(f'Required Strength: {self._itemdata["reqstr"]}')

        mods = [
            enhancement for enhancement in self._attributes['enhancements']
            if enhancement.stat == 'item_singleskill']
        if mods and self.is_identified:
            for mod in mods:
                skill_data = GameData.skills[mod.param]
                self._levelreq = max(self._levelreq, int(skill_data['reqlevel'] or 1))

        # handle level requirement
        if self._levelreq > 1 and self.is_identified:
            block.append(f'Required Level: {self._levelreq}')

        # handle weapon class and attack speed
        weapon_classes = {
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
            'h2h2': 'h2h2',
        }
        if self._itemdata['kind'] == 'weapons':
            weapon_class = GameData.get_string(
                f'weapondesc{weapon_classes[self._itemdata["type"]]}')
            speed = int(self._itemdata['speed'] or 0)
            block.append(f'{weapon_class} - [{speed}] Attack Speed')

        print(self.display_name)
        print(self._attributes)
        print(list(stat.stat for stat in self._attributes['enhancements']))

        # handle magical properties
        if self.quality.value >= ItemQuality.MAGICAL.value and not self.is_identified:
            block.append(f'{colorama.Fore.RED}Unidentified{colorama.Fore.RESET}')
        elif 'enhancements' in self._attributes:
            for enhancement in self._attributes['enhancements']:
                if enhancement.is_visible:
                    block.append(f'{colorama.Fore.BLUE}{enhancement}{colorama.Fore.RESET}')

        # handle blunt weapons
        if (self._itemdata['kind'] == 'weapons' and
                weapon_classes[self._itemdata['type']] in ['mace', 'staff']):
            block.append(f'{colorama.Fore.BLUE}+50% Damage to Undead{colorama.Fore.RESET}')

        # handle sockets
        if self.is_socketed:
            block.append(
                f'{colorama.Fore.BLUE}Socketed '
                f'({self._attributes["socket_count"]}){colorama.Fore.RESET}')

        return '\n'.join(block)
