
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

        # is extended?
        return ExtendedItem(buffer, offset)

    def __init__(self, buffer, offset):
        '''
        constructor
        '''
        self._buffer = buffer
        self._offset = offset

        if self._header != 'JM':
            raise ValueError('invalid save: mismatched item data header')

    @property
    def _header(self):
        '''
        produce the header of the item section - should be 'JM'
        '''
        return self._buffer[self._offset:self._offset + 2].decode('ascii')

    @property
    def is_identified(self):
        '''
        indicate whether the item is identified
        '''
        return bool(self._buffer.getbits(self._offset * 8 + 20, 1))

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
    def length(self):
        '''
        the length of the item in bytes (to be overwritten by subclass)
        '''
        raise NotImplementedError()

    @property
    def rawdata(self):
        '''
        the raw data of the item
        '''
        return self._buffer[self._offset:self._offset + self.length]


class SimpleItem(Item):
    '''
    save data related to a simple item that is not an ear
    '''
    def __init__(self, buffer, offset):
        '''
        constructor
        '''
        super().__init__(buffer, offset)
        self._itemdata = GameData.itemdata[self.type]

    @property
    def type(self):
        '''
        the type of the item
        '''
        num = self._buffer.getbits(self._offset * 8 + 76, 32)
        return struct.pack('<L', num).decode('ascii').strip()

    @property
    def name(self):
        '''
        the name of the item
        '''
        return GameData.get_string(self._itemdata['namestr'])

    @property
    def display_name(self):
        '''
        this item is always displayed with its base name
        '''
        return self.name

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

        if 'spelldescstr' in self._itemdata and self._itemdata['spelldescstr'] and self._itemdata['spelldesc'] == '1':
            block.append('Item Level: 1')
            block.append(GameData.get_string(self._itemdata['spelldescstr']))

        if self._itemdata['type'] in ['rune', 'gema', 'gemt', 'gems', 'geme', 'gemr', 'gemd', 'gemz']:
            block.append('Item Level 1')
            block.append('Can be Inserted into Socketed Items')

            gem = GameData.gems[self._itemdata["code"]]
            # print(gem)
            weapon_mod = GameData.properties[gem['weaponMod1Code']]
            # print(weapon_mod)

            item_stat_cost = next((isc for isc in GameData.itemstatcost if isc['Stat'] == weapon_mod['stat1']), None)
            # print(item_stat_cost)
            block.append(f'\nWeapons: {gem["weaponMod1Min"]} {gem["weaponMod1Code"]}')
            block.append(f'Armor: {None}')
            block.append(f'Helms: {None}')
            block.append(f'Shields: {None}')

        if self._itemdata['levelreq'] and int(self._itemdata['levelreq']) > 1:
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
        return f'''\
{self.name}
{self.character_class}
{self.character_level}'''


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

        if 'levelreq' in self._itemdata and self._itemdata['levelreq']:
            self._immediate_mods['levelreq'] = int(self._itemdata['levelreq'])

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
                    self._immediate_mods['levelreq'] = max(self._immediate_mods.get('levelreq', 1), int(affix_info['levelreq']))
            affix = self._buffer.getbits(self._offset * 8 + pos, 11)
            pos += 11
            self._attributes['magic_suffix'] = affix
            if affix:
                affix_info = GameData.magicsuffix[affix]
                if affix_info['levelreq']:
                    self._immediate_mods['levelreq'] = max(self._immediate_mods.get('levelreq', 1), int(affix_info['levelreq']))

        # set item details part 1
        if self.quality == ItemQuality.SET:
            self._attributes['set_id'] = self._buffer.getbits(self._offset * 8 + pos, 12)
            print(self._attributes)
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
                        self._immediate_mods['levelreq'] = max(self._immediate_mods.get('levelreq', 1), int(affix_info['levelreq']))
                    pos += 12
                else:
                    pos += 1
                if self._buffer.getbits(self._offset * 8 + pos, 1):
                    affix = self._buffer.getbits(self._offset * 8 + pos + 1, 11)
                    self._attributes[f'rare_suffix_{i}'] = affix
                    affix_info = GameData.magicsuffix[affix]
                    if affix_info['levelreq']:
                        self._immediate_mods['levelreq'] = max(self._immediate_mods.get('levelreq', 1), int(affix_info['levelreq']))
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
                    self._attributes[f'crafted_prefix_{i}'] = self._buffer.getbits(self._offset * 8 + pos + 1, 11)
                    pos += 12
                else:
                    pos += 1
                if self._buffer.getbits(self._offset * 8 + pos, 1):
                    self._attributes[f'crafted_suffix_{i}'] = self._buffer.getbits(self._offset * 8 + pos + 1, 11)
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
            # unknown bits
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
        if self._itemdata['kind'] in ['weapons', 'misc'] and self._itemdata['stackable'] == '1':
            self._attributes['quantity'] = self._buffer.getbits(self._offset * 8 + pos, 9)
            pos += 9

        # socketed items
        if self.is_socketed:
            self._attributes['socket_count'] = self._buffer.getbits(self._offset * 8 + pos, 4)
            pos += 4

        # set details part 2
        if self.quality == ItemQuality.SET:
            set_properties = self._buffer.getbits(self._offset * 8 + pos, 5)
            pos += 5

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
                val = {}
                if item_stat_cost['Save Param Bits'] and int(item_stat_cost['Save Param Bits']):
                    field_width = int(item_stat_cost['Save Param Bits'])
                    val['p'] = self._buffer.getbits(self._offset * 8 + pos, field_width)
                    pos += field_width
                if item_stat_cost['Save Bits'] and int(item_stat_cost['Save Bits']):
                    field_width = int(item_stat_cost['Save Bits'])
                    val['v'] = self._buffer.getbits(self._offset * 8 + pos, field_width)
                    if item_stat_cost['Save Add'] and int(item_stat_cost['Save Add']):
                        val['v'] -= int(item_stat_cost['Save Add'])
                    pos += field_width
                group.append({'eid': _eid, 'val': val})
                # process immediate effects
                self._immediate_mods[item_stat_cost['Stat']] = val['v']
                if item_stat_cost['Stat'] == 'item_singleskill':
                    skill_data = GameData.skills[val['p']]
                    if skill_data['reqlevel']:
                        self._immediate_mods['levelreq'] = max(self._immediate_mods.get('levelreq', 1), int(skill_data['reqlevel']))
            group[0]['children'] = group[1:]
            enhancements.append(group[0])

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
                    val = {}
                    if item_stat_cost['Save Param Bits'] and int(item_stat_cost['Save Param Bits']):
                        field_width = int(item_stat_cost['Save Param Bits'])
                        val['p'] = self._buffer.getbits(self._offset * 8 + pos, field_width)
                        pos += field_width
                    if item_stat_cost['Save Bits'] and int(item_stat_cost['Save Bits']):
                        field_width = int(item_stat_cost['Save Bits'])
                        val['v'] = self._buffer.getbits(self._offset * 8 + pos, field_width)
                        if item_stat_cost['Save Add'] and int(item_stat_cost['Save Add']):
                            val['v'] -= int(item_stat_cost['Save Add'])
                        pos += field_width
                    group.append({'eid': _eid, 'val': val})
                    # process immediate effects
                    self._immediate_mods[item_stat_cost['Stat']] = val['v']
                    if item_stat_cost['Stat'] == 'item_singleskill':
                        skill_data = GameData.skills[val['p']]
                        if skill_data['reqlevel']:
                            self._immediate_mods['levelreq'] = max(self._immediate_mods.get('levelreq', 1), int(skill_data['reqlevel']))
                group[0]['children'] = group[1:]
                set_enhancements.append(group[0])

        # sort enhancements
        def sort_enhancements(enhancement):
            '''
            a key function to sort the list of enhancements
            '''
            key_1 = int(GameData.itemstatcost[enhancement['eid']]['descpriority'] or 0)
            key_2 = 0

            if enhancement['eid'] == 107:
                key_2 = enhancement['val']['p']

            return (key_1, key_2)

        enhancements.sort(key=sort_enhancements, reverse=True)
        self._attributes['enhancements'] = enhancements

        if self.quality == ItemQuality.SET:
            set_enhancements.sort(key=sort_enhancements, reverse=True)
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
            print(self._attributes)
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

        # tomes are weird
        if self._itemdata['type'] == 'book':
            block.append('Insert Scrolls\nRight Click to Use')
        else:
            block.append(f'Item Level: {self.ilvl}')

        # charms are also weird
        if GameData.itemtypes[self._itemdata['type']]['Equiv1'] == 'char':
            block.append('Keep in Inventory to Gain Bonus')

        # jewels are special
        if self._itemdata['code'] == 'jew':
            block.append('Can be Inserted into Socketed Items')

        if 'defense' in self._attributes:
            defense = self._attributes['defense']
            if 'item_armor_percent' in self._immediate_mods:
                new_defense = (defense * (100 + self._immediate_mods['item_armor_percent'])) // 100
                if new_defense > defense:
                    block.append(f'Defense: {colorama.Fore.BLUE}{new_defense}{colorama.Fore.RESET}')
                else:
                    block.append(f'Defense: {defense}')
            else:
                block.append(f'Defense: {defense}')
        if self._itemdata['type'] in ['shie', 'head']:
            chance = int(self._itemdata['block']) + 20  # assuming a non-proficient class
            if 'toblock' in self._immediate_mods:
                chance += int(self._immediate_mods['toblock'])
            block.append(f'Chance to Block: {colorama.Fore.BLUE}{chance}%{colorama.Fore.RESET}')
        if 'minmisdam' in self._itemdata and self._itemdata['minmisdam'] and int(self._itemdata['minmisdam']):
            block.append(f'Throw Damage: {self._itemdata["minmisdam"]} to {self._itemdata["maxmisdam"]}')
        if 'mindam' in self._itemdata and self._itemdata['mindam'] and int(self._itemdata['mindam']):
            if 'maxdamage' in self._immediate_mods:
                maxdamage = int(self._itemdata['maxdam']) + self._immediate_mods['maxdamage']
                block.append(f'One-Hand Damage: {colorama.Fore.BLUE}{self._itemdata["mindam"]} to {maxdamage}{colorama.Fore.RESET}')
            else:
                block.append(f'One-Hand Damage: {self._itemdata["mindam"]} to {self._itemdata["maxdam"]}')
        if '2handmindam' in self._itemdata and self._itemdata['2handmindam'] and int(self._itemdata['2handmindam']):
            block.append(f'Two-Hand Damage: {self._itemdata["2handmindam"]} to {self._itemdata["2handmaxdam"]}')

        if 'quantity' in self._attributes:
            block.append(f'Quantity: {self._attributes["quantity"]}')
        elif 'durability' in self._attributes:
            durability = self._attributes['durability']
            max_durability = self._attributes['max_durability']
            if 'item_maxdurability_percent' in self._immediate_mods:
                max_durability = (max_durability * (100 + int(self._immediate_mods['item_maxdurability_percent']))) // 100
            block.append(f'Durability: {durability} of {max_durability}')
        if 'type' in self._itemdata and self._itemdata['type']:
            item_class = GameData.itemtypes[self._itemdata['type']]
            if item_class['Class']:
                block.append(f'{colorama.Fore.RED}({GameData.get_string("partychar" + item_class["Class"])} Only){colorama.Fore.RESET}')
        if 'reqdex' in self._itemdata and self._itemdata['reqdex'] and int(self._itemdata['reqdex']):
            block.append(f'Required Dexterity: {self._itemdata["reqdex"]}')
        if 'reqstr' in self._itemdata and self._itemdata['reqstr'] and int(self._itemdata['reqstr']):
            block.append(f'Required Strength: {self._itemdata["reqstr"]}')
        if 'levelreq' in self._immediate_mods and int(self._immediate_mods['levelreq']) > 1:
            block.append(f'Required Level: {self._immediate_mods["levelreq"]}')

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
            weapon_class = GameData.get_string(f'weapondesc{weapon_classes[self._itemdata["type"]]}')
            speed = int(self._itemdata['speed'] or 0)
            block.append(f'{weapon_class} - [{speed}] Attack Speed')

        if self.quality.value >= ItemQuality.MAGICAL.value and not self.is_identified:
            block.append(f'{colorama.Fore.RED}Unidentified{colorama.Fore.RESET}')
        elif 'enhancements' in self._attributes:
            for enhancement in self._attributes['enhancements']:
                value = enhancement['val']
                key = enhancement['eid']
                item_stat_cost = GameData.itemstatcost[key]
                # special cases
                if item_stat_cost['Stat'] == 'poisonmindam':
                    poisonmindam = value['v']
                    poisonmaxdam = enhancement['children'][0]['val']['v']
                    poisonlength = enhancement['children'][1]['val']['v']
                    if poisonmindam == poisonmaxdam:
                        str1_key = 'strModPoisonDamage'
                        line = GameData.get_string(str1_key) % (int(poisonmindam / 256 * poisonlength), int(poisonlength / 25))
                    else:
                        str1_key = 'strModPoisonDamageRange'
                        line = GameData.get_string(str1_key) % (int(poisonmindam / 256 * poisonlength), int(poisonmaxdam / 256 * poisonlength), int(poisonlength / 25))
                    block.append(f'{colorama.Fore.BLUE}{line}{colorama.Fore.RESET}')
                elif item_stat_cost['Stat'] == 'firemindam':
                    firemindam = value['v']
                    firemaxdam = enhancement['children'][0]['val']['v']
                    if firemindam == firemaxdam:
                        str1_key = 'strModFireDamage'
                        line = GameData.get_string(str1_key) % firemindam
                    else:
                        str1_key = 'strmodfiredamagerange'
                        line = GameData.get_string(str1_key) % (firemindam, firemaxdam)
                    block.append(f'{colorama.Fore.BLUE}{line}{colorama.Fore.RESET}')
                elif item_stat_cost['descfunc'] and int(item_stat_cost['descfunc']):
                    desc_func = int(item_stat_cost['descfunc'])
                    if desc_func == 1:
                        str1_key = 'descstrpos' if value['v'] >= 0 else 'descstrneg'
                        line = f'{GameData.get_string(item_stat_cost[str1_key])}'
                        desc_val = int(item_stat_cost['descval'])
                        if desc_val == 1:
                            line = f'+{value["v"]} {line}'
                        elif desc_val == 2:
                            line = f'{line} +{value["v"]}'
                    elif desc_func == 2:
                        str1_key = 'descstrpos' if value['v'] >= 0 else 'descstrneg'
                        line = f'{GameData.get_string(item_stat_cost[str1_key])}'
                        desc_val = int(item_stat_cost['descval'])
                        if desc_val == 1:
                            line = f'{value["v"]}% {line}'
                        elif desc_val == 2:
                            line = f'{line} {value["v"]}%'
                    elif desc_func == 3:
                        str1_key = 'descstrpos' if value['v'] >= 0 else 'descstrneg'
                        line = f'{GameData.get_string(item_stat_cost[str1_key])}'
                        desc_val = int(item_stat_cost['descval'])
                        if desc_val == 1:
                            line = f'{value["v"]} {line}'
                        elif desc_val == 2:
                            line = f'{line} {value["v"]}'
                    elif desc_func == 4:
                        str1_key = 'descstrpos' if value['v'] >= 0 else 'descstrneg'
                        line = f'{GameData.get_string(item_stat_cost[str1_key])}'
                        desc_val = int(item_stat_cost['descval'])
                        if desc_val == 1:
                            line = f'+{value["v"]}% {line}'
                        elif desc_val == 2:
                            line = f'{line} +{value["v"]}%'
                    elif desc_func == 11:
                        str1_key = 'descstrpos' if value['v'] >= 0 else 'descstrneg'
                        line = GameData.get_string(item_stat_cost[str1_key]) % (1, 100 // value['v'])
                    elif desc_func == 15:
                        str1_key = 'descstrpos' if value['v'] >= 0 else 'descstrneg'
                        skill_data = GameData.skills[value['p'] >> 6]
                        skill_desc = GameData.skilldesc[skill_data['skilldesc']]
                        skill_name = GameData.get_string(skill_desc['str name'])
                        line = GameData.get_string(item_stat_cost[str1_key]) % (value['v'], value['p'] & 0b111111, skill_name)
                    elif desc_func == 27:
                        str1_key = 'descstrpos' if value['v'] >= 0 else 'descstrneg'
                        skill_data = GameData.skills[value['p']]
                        skill_desc = GameData.skilldesc[skill_data['skilldesc']]
                        skill_name = GameData.get_string(skill_desc['str name'])
                        line = f'+{value["v"]} to {skill_name} ({GameData.get_string("partychar" + skill_data["charclass"])} Only)'

                        # 5   '{value*100/128}% {string1}'
                        # 6   '+{value} {string1} {string2}'
                        # 7   '{value}% {string1} {string2}'
                        # 8   '+{value}% {string1} {string2}'
                        # 9   '{value} {string1} {string2}'
                        # 10   '{value*100/128}% {string1} {string2}'
                        # 12   '+{value} {string1}'
                        # 13   '+{value} to {class} Skill Levels'
                        # 14   '+{value} to {skilltab} Skill Levels ({class} Only)'
                        # 16   'Level {sLvl} {skill} Aura When Equipped '
                        # 17   '{value} {string1} (Increases near {time})'
                        # 18   '{value}% {string1} (Increases near {time})'
                        # 19   "this is used by stats that use Blizzard's sprintf implementation (if you don't know what that is, it won't be of interest to you eitherway I guess), look at how prismatic is setup, the string is the format that gets passed to their sprintf spinoff."
                        # 20   '{value * -1}% {string1}'
                        # 21   '{value * -1} {string1}'
                        # 22   "{value}% {string1} {montype} (warning: this is bugged in vanilla and doesn't work properly, see CE forum)"
                        # 23   '{value}% {string1} {monster}'
                        # 24   'used for charges, we all know how that desc looks '
                        # 25   "not used by vanilla, present in the code but I didn't test it yet"
                        # 26   "not used by vanilla, present in the code but I didn't test it yet"
                        # 28   '+{value} to {skill}'
                    else:
                        line = f'[{desc_func}]{(key, value)}: {GameData.itemstatcost[key]["Stat"]}'
                        raise NotImplementedError(line)
                    block.append(f'{colorama.Fore.BLUE}{line}{colorama.Fore.RESET}')
                if block[-1] == block[-2]:
                    block = block[:-1]

        if self._itemdata['kind'] == 'weapons' and weapon_classes[self._itemdata['type']] in ['mace', 'staff']:
            block.append(f'{colorama.Fore.BLUE}+50% Damage to Undead{colorama.Fore.RESET}')

        if self.is_socketed:
            block.append(f'{colorama.Fore.BLUE}Socketed ({self._attributes["socket_count"]}){colorama.Fore.RESET}')

        return '\n'.join(block)