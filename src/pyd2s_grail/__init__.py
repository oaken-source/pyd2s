'''
organize a plugy stash
'''

import re
import json
import tomllib
import logging
import argparse
import operator
from functools import reduce

from pyd2s import SaveFile
from pyd2s.item import ItemLocation
from pyd2s.gamedata import GameData
from pyd2s.plugydata import PlugyStashPage

parser_config = [
    (['filename'], {
        'help': 'the path to the shared stash file'}),
    (['stashes'], {
        'nargs': '*',
        'help': 'the path to additional stash files'}),
    (['-v', '--verbose'], {
        'action': 'count', 'default': 0,
        'help': 'increase verbosity. useful for debugging'}),
    (['-B', '--backup'], {
        'action': 'store_true',
        'help': 'make backups before writing stash files'}),
    (['-o', '--reorganize'], {
        'action': 'store_true',
        'help': 'reorganize the stash'}),
    (['-c', '--config'], {
        'metavar': 'CONFIG',
        'help': 'a config defining how items are moved and organized'}),
]

parser = argparse.ArgumentParser(
    prog='pyd2s_grail',
    description='rate organize a diablo 2 PlugY holy grail stash'
)
for parser_arg in parser_config:
    parser.add_argument(*parser_arg[0], **parser_arg[1])


def applies(obj, comparable):
    '''
    a comparison helper between objects and iterables
    '''
    return not set(comparable if isinstance(comparable, list) else [comparable]).isdisjoint(
            set(obj if isinstance(obj, list) else [obj]))


class Grail:
    '''
    the layout of the grail stash
    '''
    def __init__(self, sss, config):
        '''
        constructor
        '''
        self._config = config
        self._sss = sss

        self._sections = {section['key']: GrailSection(**section) for section in config['section']}
        self._matches = [GrailMatch(**match) for match in config.get('match', [])]

    def place(self, item):
        '''
        attempt to place an item in the grail stash
        '''
        matches = [match for match in self._matches if match.applies(item)]
        rules = reduce(operator.__or__, (match.rules for match in matches), {})

        # expand the limit_columns parameter
        if 'limit_columns' in rules and not isinstance(rules['limit_columns'], list):
            limit_columns = rules['limit_columns']
            match = next(match for match in reversed(matches) if 'limit_columns' in match.rules)
            all_items = match.all_items
            item_num = all_items.index(item.type)
            limit_columns = list(range(item_num * limit_columns, (item_num + 1) * limit_columns))

            rules['limit_columns'] = limit_columns

        section = rules.pop('section', 'overflow')

        logging.debug('  section %s with rules %s', section, rules)
        res = self._sections[section].place(item, **rules)
        if not res:
            res = self._sections['overflow'].place(item)
        return res

    def flush(self, backup=False):
        '''
        put all items into the stash file
        '''
        for section in self._sections:
            logging.debug('writing stash section %s', section)
            self._sections[section].append_to(self._sss)
        self.fix_flags()
        self._sss.flush(backup)

    def fix_flags(self):
        '''
        fix the flags of the grail pages for correct indexes and shared state
        '''
        for (i, page) in enumerate(self._sss.pages):
            flags = 0
            if self._sss.type == SaveFile.Type.SSS:
                flags |= PlugyStashPage.Flags.SHARED.value
            if i == 0 or not (i + 1) % 10:
                flags |= PlugyStashPage.Flags.INDEX.value
            if i == 0 or not (i + 1) % 100:
                flags |= PlugyStashPage.Flags.MAIN_INDEX.value
            page.flags = flags


class GrailSection:
    '''
    a section of the grail stash
    '''
    def __init__(self,
                 key,
                 overflow='extend',
                 crafting_inventory=False,
                 align=1):
        '''
        constructor
        '''
        self._key = key
        self._overflow = overflow
        self._crafting_inventory = crafting_inventory
        self._align = align

        self._pages = []

    def place(self,
              item,
              limit_columns=None,
              **rules):
        '''
        place an item in the section
        '''
        # attempt to place the item on a matching page
        if limit_columns is not None:
            page_begin = min(limit_columns) // 10
            page_end = max(limit_columns) // 10

            for page in range(page_begin, page_end + 1):
                columns = [c % 10 for c in limit_columns
                           if page * 10 <= c < (page + 1) * 10]
                logging.debug('  considering columns %s on page %s', columns, page)
                if pos := self.get_page(page, create=True).place(
                        item, limit_columns=columns, **rules):
                    logging.debug('  placed in page %s at %s', page, pos)
                    return pos
        else:
            for page in range(len(self._pages) + 1):
                logging.debug('  considering page %s', page)
                if pos := self.get_page(page, create=True).place(
                        item, **rules):
                    logging.debug('  placed in page %s at %s', page, pos)
                    return pos

        # if no matching page is available, fail
        logging.debug('  could not place in %s', limit_columns)
        return None

    def get_page(self, index, create=False):
        '''
        get the indexed page
        '''
        while index >= len(self._pages) and create:
            self._pages.append(GrailPage())
        return self._pages[index]

    def append_to(self, sss):
        '''
        write the section of grail data to the stash
        '''
        # pad to alignment
        while (len(sss.pages) + 1) % self._align:
            logging.debug('adding padding page #%s to stash', len(sss.pages) + 1)
            sss.append_page()

        for page in self._pages:
            logging.debug('adding item page #%s to stash', len(sss.pages) + 1)
            sss.append_page()
            for item in page.items:
                logging.debug('adding item %s to stash page %s at %s',
                              item.short_str(), len(sss.pages), item.location.get_pos())
                sss.pages[-1].put(item)


class GrailPage:
    '''
    a page of grail data
    '''
    width = 10
    height = 10

    def __init__(self):
        '''
        constructor
        '''
        self._map = [[None] * self.height for _ in range(self.width)]
        self._items = []

    def place(self, item, limit_columns=None):
        '''
        place an item on the page
        '''
        for row in range(self.height - (item.height - 1)):
            for col in limit_columns or range(self.width):
                if col + item.width > self.width:
                    continue
                if not any(self._map[col + i][row + j]
                           for i in range(item.width)
                           for j in range(item.height)):
                    self._items.append(item)
                    item.location = ItemLocation.stored(ItemLocation.StoredType.STASH, (col, row))
                    for i in range(item.width):
                        for j in range(item.height):
                            self._map[col + i][row + j] = item
                    return (col, row)

        return None

    @property
    def items(self):
        '''
        the list of items on the page
        '''
        return self._items


class GrailMatch:
    '''
    a matcher for the grail stash
    '''
    def __init__(self,
                 match_type='literal',
                 item_class=None,
                 item_type=None,
                 item_quality=None,
                 **rules):
        '''
        constructor
        '''
        def expand_regex(regex, haystack):
            '''
            expand a regex or list of regexes to all possible values
            '''
            if isinstance(regex, list):
                return [val for reg in regex for val in expand_regex(reg, haystack)]
            return [hay for hay in haystack if re.match(regex, hay)]

        # expand all regex matchers to all possible game values
        if match_type == 'regex':
            if item_class is not None:
                item_class = expand_regex(
                    item_class,
                    [item['code'] for item in GameData.itemdata.values()])
            if item_type is not None:
                item_type = expand_regex(
                    item_type,
                    [itemtype['Code'] for itemtype in GameData.itemtypes.values()])

        # include parent item types in the type matcher
        if item_type is not None:
            frontier = item_type[:]
            expanded = []
            while frontier:
                element, frontier = frontier[0], frontier[1:]
                expanded.append(element)
                frontier.extend(
                    itemtype['Code'] for itemtype in GameData.itemtypes.values()
                    if element in [itemtype['Equiv1'], itemtype['Equiv2']])
            item_type = expanded

        self._item_class = item_class
        self._item_type = item_type
        self._item_quality = item_quality

        self._rules = rules

    def applies(self, item):
        '''
        match comparator for the given filters
        '''
        return (
            (self._item_class is None or applies(item.type, self._item_class)) and
            (self._item_type is None or applies(item.item_types, self._item_type)) and
            (self._item_quality is None or applies(item.quality.value, self._item_quality)))

    @property
    def all_items(self):
        '''
        all possible item types this match object could apply to
        '''
        return [
            item['code'] for item in GameData.itemdata.values() if
            (self._item_class is None or applies(item['code'], self._item_class)) and
            (self._item_type is None or applies([item['type'], item['type2']], self._item_type))]

    @property
    def rules(self):
        '''
        the rules section of the match object
        '''
        return self._rules


def pyd2s_grail(argv=None):
    '''
    main entry point
    '''
    args = parser.parse_intermixed_args(argv)

    # set the logging verbosity
    logging.basicConfig(level=30 - args.verbose * 10)

    # initialize a default sorting config
    config = tomllib.loads('''
[[section]]
key = "overflow"
''')

    # and replace with the given config, if any
    if args.config:
        with open(args.config, 'rb') as toml:
            config = tomllib.load(toml)

    logging.debug(json.dumps(config, indent=4))

    # open the output stash file, making sure it's actually a PlugY stash
    sss = SaveFile.open(args.filename)
    if sss.type not in [SaveFile.Type.SSS, SaveFile.Type.D2X]:
        raise ValueError(f'unsupported stash type: {sss.type}')

    items = []

    # if we reorganize, pull all items from the stash
    if args.reorganize:
        items.extend(sss.clear())

    # if we add from other, pull all items from those
    source_stashes = []
    if args.stashes:
        for stash in args.stashes:
            d2s = SaveFile.open(stash)
            if d2s.type in [SaveFile.Type.D2X, SaveFile.Type.SSS]:
                # take all files from stash files
                source_stashes.append(d2s)
                items.extend(d2s.clear())
            if d2s.type == SaveFile.Type.D2S:
                # this could get weird, since PlugY overwrites the stash inventory
                # it could happen that we would pull items from the stash into itself
                # so I'm skipping that for now.
                raise NotImplementedError()
            if d2s.type == SaveFile.Type.D2I:
                # individual item, shouldn't be too difficult
                items.append(d2s.item)

    grail = Grail(sss, config)

    for item in items:
        logging.debug('attempting to place item %s in grail stash',
                      item.short_str())
        if not grail.place(item):
            raise ValueError(f'unable to place item {item.short_str()}')

    grail.flush(args.backup)
    for stash in source_stashes:
        stash.flush(args.backup)
