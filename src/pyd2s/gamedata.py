
'''
this module provides access to the games data files
'''

import os
import csv
import struct
import logging


class _GameData:
    '''
    provide access to the games data files
    '''

    _TABLE_ALIAS = {
        'itemdata': ['armor', 'weapons', 'misc'],
        'rareaffix': ['raresuffix', 'rareprefix']
    }
    _TABLE_PRIMARY_KEYS = {
        'itemdata': 'code',
        'armor': 'code',
        'weapons': 'code',
        'misc': 'code',
        'itemtypes': 'Code',
        'skilldesc': 'skilldesc',
        'gems': 'code',
        'properties': 'code',
        'runes': 'Name',
    }
    _TABLE_INDICES = {
        'itemstatcost': 'Stat',
        'playerclass': 'Code',
    }
    _TABLE_INDEX_OFFSETS = {
        'magicprefix': 1,
        'magicsuffix': 1,
        'rareaffix': 1,
    }
    _TABLE_INDEX_SKIPS_EXPANSION = {
        'charstats',
        'setitems',
        'uniqueitems',
    }

    def __init__(self):
        '''
        constructor
        '''
        self._tables = {}
        self._expansion = True

    def set_expansion(self, value):
        '''
        set whether we are looking at expansion or classic data files
        '''
        self._expansion = value

    def __getattr__(self, table):
        '''
        produce a data table for the given key
        '''
        if self._expansion not in self._tables:
            self._tables[self._expansion] = {}

        if table not in self._tables[self._expansion]:
            if table == 'strings':
                self._tables[self._expansion][table] = self._load_strings()
            elif table.endswith('_index'):
                self._tables[self._expansion][table] = self._load_index_table(table)
            else:
                self._tables[self._expansion][table] = self._load_table(table)

        return self._tables[self._expansion][table]

    def _load_table(self, table):
        '''
        load a data table into memory on first access
        '''
        if table in self._TABLE_PRIMARY_KEYS:
            return self._load_table_as_dict(table, self._TABLE_PRIMARY_KEYS[table])
        return self._load_table_as_list(table, self._TABLE_INDEX_OFFSETS.get(table, 0))

    def _load_table_as_dict(self, table, primary_key):
        '''
        load a data table into memory as a key-indexed dictionary
        '''
        entries = {}

        if table in self._TABLE_ALIAS:
            for subtable in self._TABLE_ALIAS[table]:
                subtable_entries = self._load_table_as_dict(subtable, primary_key)
                for entry in subtable_entries:
                    subtable_entries[entry]['kind'] = subtable
                entries.update(subtable_entries)
            return entries

        base = f'gamedata/d2{"exp" if self._expansion else "data"}/data/global/excel/'

        with open(os.path.join(base, f'{table}.txt'), 'r', encoding='cp1252') as csvfile:
            lines = csvfile.readlines()
        data_source = (line for line in lines)
        if table in self._TABLE_INDEX_SKIPS_EXPANSION:
            data_source = filter(lambda e: not e.startswith('Expansion'), data_source)

        reader = csv.DictReader(data_source, delimiter='\t')
        entries = {row[primary_key]: row for row in reader}

        return entries

    def _load_table_as_list(self, table, index_offset):
        '''
        load a data table into memory as 0 or 1 indexed a list
        '''
        entries = [None] * index_offset

        if table in self._TABLE_ALIAS:
            for subtable in self._TABLE_ALIAS[table]:
                entries.extend(self._load_table_as_list(subtable, 0))
            return entries

        base = f'gamedata/d2{"exp" if self._expansion else "data"}/data/global/excel/'

        with open(os.path.join(base, f'{table}.txt'), 'r', encoding='cp1252') as csvfile:
            lines = csvfile.readlines()
        data_source = (line for line in lines)
        if table in self._TABLE_INDEX_SKIPS_EXPANSION:
            data_source = filter(lambda e: not e.startswith('Expansion'), data_source)

        reader = csv.DictReader(data_source, delimiter='\t')
        entries = list(reader)

        # fix incorrect usage of ModStre9t
        if table == 'itemstatcost':
            for entry in entries:
                if entry['descstrpos'] == 'ModStre9t':
                    entry['descstrpos'] = 'ModStre9u'
                if entry['descstrneg'] == 'ModStre9t':
                    entry['descstrneg'] = 'ModStre9u'

        return entries

    def _load_index_table(self, index_table):
        '''
        load an index for an existing table
        '''
        table = getattr(self, index_table.removesuffix('_index'))
        key = self._TABLE_INDICES[index_table.removesuffix('_index')]

        entries = {row[key]: row for row in table}

        return entries

    def _load_strings(self):
        '''
        load the string table into memory on first access
        '''
        string_tbl_classic = [
            'gamedata/d2data/data/local/lng/eng/string.tbl']
        string_tbl_expansion = [
            'gamedata/d2exp/data/local/lng/eng/expansionstring.tbl',
            'gamedata/d2exp/data/local/lng/eng/patchstring.tbl']

        entries = {}
        for tbl in string_tbl_classic:
            entries.update(self._load_string_tbl(tbl))
        if self._expansion:
            for tbl in string_tbl_expansion:
                entries.update(self._load_string_tbl(tbl))

        return entries

    def _load_string_tbl(self, filename):
        '''
        load one string table file into memory
        '''
        with open(filename, 'rb') as tbl:
            data = tbl.read()

        pos = 0
        num_entries = struct.unpack_from('<H', data, pos + 2)[0]

        pos = 21
        entries = []
        for i in range(num_entries):
            entries.append(struct.unpack_from('<H', data, pos + 2 * i)[0])

        pos = 21 + num_entries * 2
        entry_dict = {}
        for entry in entries:
            _pos = pos + entry * 17
            key_offset = struct.unpack_from('<L', data, _pos + 7)[0]
            val_offset = struct.unpack_from('<L', data, _pos + 11)[0]

            key = data[key_offset:data.index(0, key_offset)].decode('cp1252').lower()
            val = data[val_offset:data.index(0, val_offset)].decode('cp1252')

            if key not in entry_dict:
                entry_dict[key] = val

        return entry_dict

    def get_string(self, key):
        '''
        produce a string from the string.tbl files
        '''
        res = self.strings.get(key.lower(), key)
        logging.debug('string.tbl:%s:%s', key, res)
        return res

    def get_consecutive_item_stat_blocks(self, eid):
        '''
        indicate how many stat blocks follow implicitly from the given first one
        '''
        # I think this is hard coded in the game
        item_stat_cost = self.itemstatcost[eid]
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


GameData = _GameData()
