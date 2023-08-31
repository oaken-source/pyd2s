
'''
this module provides access to the games data files
'''

import os
import csv
import struct


class GameData:
    '''
    provide access to the games data files
    '''

    _is_expansion = True
    _itemdata = {}

    _lq_name_prefix = {}
    _hq_name_prefix = {}
    _magic_prefix = {}
    _magic_suffix = {}
    _rare_affix = {}

    _item_stat_cost = {}
    _item_class = {}

    _skills = {}

    _strings = {}

    @classmethod
    def set_expansion(cls, value):
        '''
        set whether we are looking at expansion or classic data files
        '''
        cls.is_expansion = value

    @classmethod
    def get_itemdata(cls, code):
        '''
        produce the item data for a given item code
        '''
        if cls._is_expansion not in cls._itemdata:
            cls._itemdata[cls._is_expansion] = cls._read_itemdata()

        return cls._itemdata[cls._is_expansion][code.strip()]

    @classmethod
    def _read_itemdata(cls):
        '''
        read the item data from the game files
        '''
        base_path = f'gamedata/d2{"exp-1.14d" if cls._is_expansion else "data"}/data/global/excel/'
        res = {}
        for file in ['misc', 'armor', 'weapons']:
            with open(os.path.join(base_path, f'{file}.txt'), 'r', encoding='ascii') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                items = { row['code']: row | {'kind': file} for row in reader }
            res.update(items)
        return res

    @classmethod
    def get_lq_name_prefix(cls, key):
        '''
        produce the low quality prefix data for a given prefix id
        '''
        if cls._is_expansion not in cls._lq_name_prefix:
            cls._lq_name_prefix[cls._is_expansion] = cls._read_lq_name_prefix_data()

        return cls._lq_name_prefix[cls._is_expansion][key]

    @classmethod
    def _read_lq_name_prefix_data(cls):
        '''
        read the prefix data from the game files
        '''
        base_path = f'gamedata/d2{"exp-1.14d" if cls._is_expansion else "data"}/data/global/excel/'
        res = []
        for file in ['lowqualityitems']:
            with open(os.path.join(base_path, f'{file}.txt'), 'r', encoding='ascii') as file:
                items = list(map(str.strip, file.readlines()[1:]))
            res.extend(items)
        return res

    @classmethod
    def get_magic_prefix(cls, key):
        '''
        produce the magic prefix data for a given prefix id
        '''
        if cls._is_expansion not in cls._magic_prefix:
            cls._magic_prefix[cls._is_expansion] = cls._read_magic_prefix_data()

        return cls._magic_prefix[cls._is_expansion][key]

    @classmethod
    def _read_magic_prefix_data(cls):
        '''
        read the prefix data from the game files
        '''
        base_path = f'gamedata/d2{"exp-1.14d" if cls._is_expansion else "data"}/data/global/excel/'
        res = ['']
        for file in ['Prefix']:
            with open(os.path.join(base_path, f'Magic{file}.txt'), 'r', encoding='ascii') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                items = [ row | {'kind': file} for row in reader if row ['Name'] != 'Expansion' ]
            res.extend(items)
        return res

    @classmethod
    def get_magic_suffix(cls, key):
        '''
        produce the magic suffix data for a given suffix id
        '''
        if cls._is_expansion not in cls._magic_suffix:
            cls._magic_suffix[cls._is_expansion] = cls._read_magic_suffix_data()

        return cls._magic_suffix[cls._is_expansion][key]

    @classmethod
    def _read_magic_suffix_data(cls):
        '''
        read the suffix data from the game files
        '''
        base_path = f'gamedata/d2{"exp-1.14d" if cls._is_expansion else "data"}/data/global/excel/'
        res = ['']
        for file in ['Suffix']:
            with open(os.path.join(base_path, f'Magic{file}.txt'), 'r', encoding='ascii') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                items = [ row | {'kind': file} for row in reader if row['Name'] != 'Expansion' ]
            res.extend(items)
        return res

    @classmethod
    def get_rare_affix(cls, key):
        '''
        produce the rare affix data for a given affix id
        '''
        if cls._is_expansion not in cls._rare_affix:
            cls._rare_affix[cls._is_expansion] = cls._read_rare_affix_data()

        return cls._rare_affix[cls._is_expansion][key]

    @classmethod
    def _read_rare_affix_data(cls):
        '''
        read the affix data from the game files
        '''
        base_path = f'gamedata/d2{"exp-1.14d" if cls._is_expansion else "data"}/data/global/excel/'
        res = ['']
        for file in ['Suffix', 'Prefix']:
            with open(os.path.join(base_path, f'Rare{file}.txt'), 'r', encoding='ascii') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                items = [ row | {'kind': file} for row in reader ]
            res.extend(items)
        return res

    @classmethod
    def get_skill(cls, key):
        '''
        produce the skill data for a given skill id
        '''
        if cls._is_expansion not in cls._skills:
            cls._skills[cls._is_expansion] = cls._read_skill_data()

        return cls._skills[cls._is_expansion][key]

    @classmethod
    def _read_skill_data(cls):
        '''
        read the skill data from the game files
        '''
        base_path = f'gamedata/d2{"exp-1.14d" if cls._is_expansion else "data"}/data/global/excel/'
        res = []
        for file in ['skills']:
            with open(os.path.join(base_path, f'{file}.txt'), 'r', encoding='ascii') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                items = list(reader)
            res.extend(items)
        return res

    @classmethod
    def get_item_stat_cost(cls, key):
        '''
        produce the item stat cost block for a given key
        '''
        if cls._is_expansion not in cls._item_stat_cost:
            cls._item_stat_cost[cls._is_expansion] = cls._read_item_stat_cost_data()

        if key >= len(cls._item_stat_cost[cls._is_expansion]):
            return None

        res = cls._item_stat_cost[cls._is_expansion][key]

        # Hack: the game seems to use the String key ModStre9u instead of ModStre9t
        if res['descstrpos'] == 'ModStre9t':
            res['descstrpos'] = 'ModStre9u'
        if res['descstrneg'] == 'ModStre9t':
            res['descstrneg'] = 'ModStre9u'


        return res

    @classmethod
    def _read_item_stat_cost_data(cls):
        '''
        read the item stat cost data from the game files
        '''
        base_path = f'gamedata/d2{"exp-1.14d" if cls._is_expansion else "data"}/data/global/excel/'
        res = []
        for file in ['ItemStatCost']:
            with open(os.path.join(base_path, f'{file}.txt'), 'r', encoding='ascii') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                items = list(reader)
            res.extend(items)
        return res

    @classmethod
    def get_consecutive_item_stat_blocks(cls, eid):
        '''
        indicate how many stat blocks follow implicitly from the given first one
        '''
        item_stat_cost = cls.get_item_stat_cost(eid)
        if item_stat_cost['Stat'] in [
                'item_maxdamage_percent',
                'firemindam',
                'lightmindam',
                'magicmindam']:
            return 2
        if item_stat_cost['Stat'] in [
                'coldmindam',
                'poisonmindam']:
            return 3
        return 1

    @classmethod
    def get_item_class(cls, key):
        '''
        produce the item class block for a given key
        '''
        if cls._is_expansion not in cls._item_class:
            cls._item_class[cls._is_expansion] = cls._read_item_class_data()

        res = cls._item_class[cls._is_expansion][key]

        return res

    @classmethod
    def _read_item_class_data(cls):
        '''
        read the item stat cost data from the game files
        '''
        base_path = f'gamedata/d2{"exp-1.14d" if cls._is_expansion else "data"}/data/global/excel/'
        res = {}
        for file in ['ItemTypes']:
            with open(os.path.join(base_path, f'{file}.txt'), 'r', encoding='ascii') as csvfile:
                reader = csv.DictReader(csvfile, delimiter='\t')
                items = { row['Code']: row for row in reader }
            res.update(items)
        return res

    @classmethod
    def get_string(cls, key):
        '''
        produce a string from the string.tbl files
        '''
        if cls._is_expansion not in cls._strings:
            cls._strings[cls._is_expansion] = cls._read_strings()

        if key not in cls._strings[cls._is_expansion]:
            return key # this is also the default behavior in the game
        return cls._strings[cls._is_expansion][key]

    @classmethod
    def _read_strings(cls):
        '''
        read the game string.tbl files in order
        '''
        res = cls._read_strings_tbl('gamedata/d2data/data/local/lng/eng/string.tbl')
        if cls._is_expansion:
            res.update(cls._read_strings_tbl('gamedata/d2exp-1.14d/data/local/LNG/ENG/expansionstring.tbl'))
            res.update(cls._read_strings_tbl('gamedata/d2exp-1.14d/data/local/LNG/ENG/patchstring.tbl'))
        return res

    @classmethod
    def _read_strings_tbl(cls, filename):
        '''
        read a strings.tbl file into a dictionary
        '''
        with open(filename, 'rb') as tbl:
            header = tbl.read(21)
            num_entries = struct.unpack_from('<H', header, 2)[0]

            entries = []
            for _ in range(num_entries):
                entries.append(struct.unpack('<H', tbl.read(2))[0])

            node_start = 21 + num_entries * 2

            entry_dict = {}
            for e in entries:
                tbl.seek(node_start + e * 17)
                hash_entry = tbl.read(17)
                key_offset = struct.unpack_from('<L', hash_entry, 7)[0]
                val_offset = struct.unpack_from('<L', hash_entry, 11)[0]

                tbl.seek(key_offset)
                key = bytearray()
                while True:
                    c = tbl.read(1)[0]
                    if c == 0:
                        break
                    key.append(c)
                key = key.decode('ascii')

                tbl.seek(val_offset)
                val = bytearray()
                while True:
                    c = tbl.read(1)[0]
                    if c == 0:
                        break
                    val.append(c)
                val = val.decode('utf-8')

                entry_dict[key] = val

        return entry_dict
