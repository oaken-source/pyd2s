
'''
this module provides access to the games data files
'''

import os
import csv
import struct


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
    }
    _TABLE_INDEX_OFFSETS = {
        'magicprefix': 1,
        'magicsuffix': 1,
        'rareaffix': 1,
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

        with open(os.path.join(base, f'{table}.txt'), 'r', encoding='ascii') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
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

        with open(os.path.join(base, f'{table}.txt'), 'r', encoding='ascii') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='\t')
            entries = list(reader)

        # fix incorrect usage of ModStre9t
        if table == 'itemstatcost':
            for entry in entries:
                if entry['descstrpos'] == 'ModStre9t':
                    entry['descstrpos'] = 'ModStre9u'
                if entry['descstrneg'] == 'ModStre9t':
                    entry['descstrneg'] = 'ModStre9u'

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
        def read_null_terminated_string(file):
            '''
            read a null-terminated string from a given file-like object
            '''
            res = bytearray()
            while True:
                next_byte = file.read(1)[0]
                if next_byte == 0:
                    break
                res.append(next_byte)
            return res.decode('utf-8')

        with open(filename, 'rb') as tbl:
            header = tbl.read(21)
            num_entries = struct.unpack_from('<H', header, 2)[0]

            entries = []
            for _ in range(num_entries):
                entries.append(struct.unpack('<H', tbl.read(2))[0])

            node_start = 21 + num_entries * 2

            entry_dict = {}
            for entry in entries:
                tbl.seek(node_start + entry * 17)
                hash_entry = tbl.read(17)
                key_offset = struct.unpack_from('<L', hash_entry, 7)[0]
                val_offset = struct.unpack_from('<L', hash_entry, 11)[0]

                tbl.seek(key_offset)
                key = read_null_terminated_string(tbl).lower()
                tbl.seek(val_offset)
                val = read_null_terminated_string(tbl)

                entry_dict[key] = val

        return entry_dict

    def get_string(self, key):
        '''
        produce a string from the string.tbl files
        '''
        return self.strings.get(key.lower(), f'{{{key}}}')

    def get_consecutive_item_stat_blocks(self, eid):
        '''
        indicate how many stat blocks follow implicitly from the given first one
        '''
        # FIXME: how can I get this info out of the game files?
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
