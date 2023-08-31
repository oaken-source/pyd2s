
'''
this module provides classes to manage item of a d2s save
'''

import math
import struct

import colorama

from pyd2s.character import Character
from pyd2s.basictypes import CharacterClass, ItemQuality
from pyd2s.gamedata import GameData


class ItemData:
    '''
    save data related to item
    '''

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
                return ItemData.SimpleItem(buffer, offset)

            # is ear?
            if buffer.getbits(offset * 8 + 32, 1):
                return ItemData.EarItem(buffer, offset)

            # is extended?
            return ItemData.ExtendedItem(buffer, offset)

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
            self._itemdata = GameData.get_itemdata(self.type)

        @property
        def type(self):
            '''
            the type of the item
            '''
            num = self._buffer.getbits(self._offset * 8 + 76, 32)
            return struct.pack('<L', num).decode('ascii')

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
            name = GameData.get_string(self._itemdata['namestr'])

            block = [name]

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
{self.character_name}'s Ear
{self.character_class}
Level {self.character_level}'''


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
            pos = 154

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
                self._attributes['magic_prefix'] = self._buffer.getbits(self._offset * 8 + pos, 11)
                pos += 11
                self._attributes['magic_suffix'] = self._buffer.getbits(self._offset * 8 + pos, 11)
                pos += 11

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
                        self._attributes[f'rare_prefix_{i}'] = self._buffer.getbits(self._offset * 8 + pos + 1, 11)
                        pos += 12
                    else:
                        pos += 1
                    if self._buffer.getbits(self._offset * 8 + pos, 1):
                        self._attributes[f'rare_suffix_{i}'] = self._buffer.getbits(self._offset * 8 + pos + 1, 11)
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
            if self.type.strip() in ['ibk', 'tbk']:
                # unknown bits
                #self._attributes['tome_unknown_bits'] = self._buffer.getbits(self._offset * 8 + pos, 5)
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
                    pos += 9 # last bit is unknown
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
                self._attributes['set_properties'] = self._buffer.getbits(self._offset * 8 + pos, 5)
                pos += 5

            # enhancements
            enhancements = []
            while True:
                eid = self._buffer.getbits(self._offset * 8 + pos, 9)
                pos += 9
                if eid == 0x1FF:
                    break
                consecutive = GameData.get_consecutive_item_stat_blocks(eid)
                for _eid in range(eid, eid + consecutive):
                    item_stat_cost = GameData.get_item_stat_cost(_eid)
                    val = {}
                    if item_stat_cost['Save Param Bits'] and int(item_stat_cost['Save Param Bits']):
                        field_width = int(item_stat_cost['Save Param Bits'])
                        val['p'] = self._buffer.getbits(self._offset * 8 + pos, field_width)
                        pos += field_width
                    if item_stat_cost['Save Bits'] and int(item_stat_cost['Save Bits']):
                        field_width = int(item_stat_cost['Save Bits'])
                        val['v'] = self._buffer.getbits(self._offset * 8 + pos, field_width)
                        pos += field_width
                    enhancements.append((_eid, val))
            self._attributes['enhancements'] = enhancements

            # mark the length of the item in bits
            self._length = pos

            #pad = 0
            #while self._buffer[self._offset + self.length] != ord('J'):
            #    pad += 1
            #    self._length += 8

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
            levelreq = 1
            name = GameData.get_string(self._itemdata['namestr'])
            if self.quality == ItemQuality.LOW_QUALITY:
                name = f'{GameData.get_lq_name_prefix(self._attributes["lq_name_prefix"])} {name}'
            if self.quality == ItemQuality.HIGH_QUALITY:
                name = f'Superior {name}'
            if self.quality.value < ItemQuality.MAGICAL.value and (self.is_socketed or self.is_ethereal):
                name = f'{colorama.Fore.LIGHTBLACK_EX}{name}{colorama.Fore.RESET}'
            if self.quality == ItemQuality.MAGICAL:
                line = f'{colorama.Fore.BLUE}'
                if self.is_identified:
                    if self._attributes['magic_prefix']:
                        affix = GameData.get_magic_prefix(self._attributes["magic_prefix"])
                        if affix['levelreq']:
                            levelreq = max(levelreq, int(affix['levelreq']))
                        line += f'{GameData.get_string(affix["Name"])} '
                    line += name
                    if self._attributes['magic_suffix']:
                        affix = GameData.get_magic_suffix(self._attributes["magic_suffix"])
                        if affix['levelreq']:
                            levelreq = max(levelreq, int(affix['levelreq']))
                        line += f' {GameData.get_string(affix["Name"])}'
                else:
                    line += name
                line += f'{colorama.Fore.RESET}'
                name = line
            if self.quality == ItemQuality.SET:
                raise NotImplementedError()
            if self.quality == ItemQuality.RARE:
                line = f'{colorama.Fore.YELLOW}'
                if self.is_identified:
                    line += f'{GameData.get_string(GameData.get_rare_affix(self._attributes["rare_name_1"])["name"])} {GameData.get_string(GameData.get_rare_affix(self._attributes["rare_name_2"])["name"])}\n'
                line += f'{colorama.Fore.YELLOW}{name}{colorama.Fore.RESET}'
                name = line
            if self.quality == ItemQuality.UNIQUE:
                raise NotImplementedError()
            if self.quality == ItemQuality.CRAFTED:
                raise NotImplementedError()

            block = [name]
            block.append(f'Item Level: {self.ilvl}')

            if 'defense' in self._attributes:
                block.append(f'Defense: {self._attributes["defense"]}')
            if self._itemdata['type'] in ['shie', 'head']:
                block.append(f'Chance to Block: {colorama.Fore.BLUE}{int(self._itemdata["block"]) + 20}%{colorama.Fore.RESET}')
            if 'mindam' in self._itemdata and self._itemdata['mindam'] and int(self._itemdata['mindam']):
                block.append(f'Damage: {self._itemdata["mindam"]} to {self._itemdata["maxdam"]}')
            if 'durability' in self._attributes:
                block.append(f'Durability: {self._attributes["durability"]} of {self._attributes["max_durability"]}')
            if 'type' in self._itemdata and self._itemdata['type']:
                item_class = GameData.get_item_class(self._itemdata['type'])
                if item_class['Class']:
                    block.append(f'{colorama.Fore.RED}({GameData.get_string("partychar" + item_class["Class"])} Only){colorama.Fore.RESET}')
            if 'reqdex' in self._itemdata and self._itemdata['reqdex'] and int(self._itemdata['reqdex']):
                block.append(f'Required Dexterity: {self._itemdata["reqdex"]}')
            if 'reqstr' in self._itemdata and self._itemdata['reqstr'] and int(self._itemdata['reqstr']):
                block.append(f'Required Strength: {self._itemdata["reqstr"]}')
            if levelreq > 1:
                block.append(f'Required Level: {levelreq}')

            if self.quality.value >= ItemQuality.MAGICAL.value and not self.is_identified:
                block.append(f'{colorama.Fore.RED}Unidentified{colorama.Fore.RESET}')
            elif 'enhancements' in self._attributes:
                for (key, value) in self._attributes['enhancements']:
                    item_stat_cost = GameData.get_item_stat_cost(key)
                    if item_stat_cost['Save Add'] and int(item_stat_cost['Save Add']):
                        value['v'] -= int(item_stat_cost['Save Add'])
                    if item_stat_cost['descfunc'] and int(item_stat_cost['descfunc']):
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
                            skill_data = GameData.get_skill(value['p'] >> 6)
                            line = GameData.get_string(item_stat_cost[str1_key]) % (value['v'], value['p'] & 0b111111, GameData.get_string(skill_data['skill']))
                        elif desc_func == 27:
                            str1_key = 'descstrpos' if value['v'] >= 0 else 'descstrneg'
                            skill_data = GameData.get_skill(value['p'])
                            line = f'+{value["v"]} to {GameData.get_string(skill_data["skill"])} ({GameData.get_string("partychar" + skill_data["charclass"])} Only)'


                            # 5   '{value*100/128}% {string1}'
                            # 6   '+{value} {string1} {string2}'
                            # 7   '{value}% {string1} {string2}'
                            # 8   '+{value}% {string1} {string2}'
                            # 9   '{value} {string1} {string2}'
                            # 10   '{value*100/128}% {string1} {string2}'
                            # 12   '+{value} {string1}'
                            # 13   '+{value} to {class} Skill Levels'
                            # 14   '+{value} to {skilltab} Skill Levels ({class} Only)'
                            # 15   '{chance}% to case {slvl} {skill} on {event}'
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
                            line = f'[{desc_func}]{(key, value)}: {GameData.get_item_stat_cost(key)["Stat"]}'
                            raise NotImplementedError(line)
                        block.append(f'{colorama.Fore.BLUE}{line}{colorama.Fore.RESET}')

            if self.is_socketed:
                block.append(f'{colorama.Fore.BLUE}Socketed ({self._attributes["socket_count"]}){colorama.Fore.RESET}')

            if 'quantity' in self._attributes:
                block.append(f'Quantity: {self._attributes["quantity"]}')

            return '\n'.join(block)

    def __init__(self, buffer, offset):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer
        self._offset = offset

        self._pdata = []
        self._cdata = []
        self._mdata = []
        self._gdata = []

        if self._header != 'JM':
            raise ValueError('invalid save: mismatched player item data section header')

        # we can stop looking for item data on a sparse input file
        if self._buffer.sparse:
            return

        ptr = self._offset + 2

        # player items
        pcount = struct.unpack_from('<H', self._buffer, ptr)[0]
        ptr += 2
        for _ in range(pcount):
            item = self.Item.from_data(self._buffer, ptr)
            ptr += item.length
            self._pdata.append(item)

        # corpse items
        ccount = 0
        if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
            raise ValueError('invalid save: mismatched corpse item data section header')
        ptr += 2
        ccount = struct.unpack_from('<H', self._buffer, ptr)[0]
        ptr += 2
        if ccount == 1:
            ptr += 12
            if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
                raise ValueError('invalid save: mismatched corpse item data section header')
            ptr += 2
            ccount = struct.unpack_from('<H', self._buffer, ptr)[0]
            ptr += 2
            for _ in range(ccount):
                item = self.Item.from_data(self._buffer, ptr)
                ptr += item.length
                self._cdata.append(item)

        # mercenary items
        if Character(self._buffer).is_expansion:
            if self._buffer[ptr:ptr+2].decode('ascii') != 'jf':
                raise ValueError('invalid save: mismatched mercenary item data section header')
            ptr += 2
            if self._buffer[ptr:ptr+2].decode('ascii') != 'JM':
                raise ValueError('invalid save: mismatched corpse item data section header')
            ptr += 2
            mcount = struct.unpack_from('<H', self._buffer, ptr)[0]
            ptr += 2
            for _ in range(mcount):
                item = self.Item.from_data(self._buffer, ptr)
                ptr += item.length
                self._mdata.append(item)
            if self._buffer[ptr:ptr+2].decode('ascii') != 'kf':
                raise ValueError('invalid save: mismatched mercenary item data section header')
            ptr += 2

        # golem items
        if Character(self._buffer).character_class == CharacterClass.NECROMANCER:
            gcount = self._buffer[ptr]
            ptr += 1
            if gcount == 1:
                item = self.Item.from_data(self._buffer, ptr)
                ptr += item.length
                self._gdata.append(item)

    @property
    def _header(self):
        '''
        produce the header of the items section - should be 'JM'
        '''
        if self._buffer.sparse:
            return 'JM'
        return self._buffer[self._offset:self._offset + 2].decode('ascii')

    @property
    def pcount(self):
        '''
        player item count
        '''
        return len(self._pdata)

    def getpdata(self, index):
        '''
        Get player item data
        '''
        return self._pdata[index]

    @property
    def ccount(self):
        '''
        corpse item count
        '''
        return len(self._cdata)

    def getcdata(self, index):
        '''
        Get corpse item data
        '''
        return self._cdata[index]

    @property
    def mcount(self):
        '''
        mercenary item count
        '''
        return len(self._mdata)

    def getmdata(self, index):
        '''
        Get mercenary item data
        '''
        return self._mdata[index]

    @property
    def gcount(self):
        '''
        iron golem item count
        '''
        return len(self._gdata)

    def getgdata(self, index):
        '''
        Get iron golem item data
        '''
        return self._gdata[index]
