'''
display diablo 2 save file information using pyd2s
'''

import os
import struct
import logging
import argparse
import datetime

import pyd2s
from pyd2s import SaveFile
from pyd2s.questdata import Quest
from pyd2s.character import Character
from pyd2s.item import ItemQuality, ExtendedItem

parser_config = [
    (['filename'], {
        'help': 'the path to the d2s file'}),
    (['-a'], {
        'action': 'store_true',
        'help': 'display all information, equivalent to -scmqwi'}),
    (['-s'], {
        'action': 'store_true',
        'help': 'display save file information'}),
    (['-c'], {
        'action': 'store_true',
        'help': 'display character information'}),
    (['-m'], {
        'action': 'store_true',
        'help': 'display mercenary information'}),
    (['-q'], {
        'action': 'store_true',
        'help': 'display quest information'}),
    (['-w'], {
        'action': 'store_true',
        'help': 'display waypoint information'}),
    (['-i'], {
        'action': 'store_true',
        'help': 'display inventory information'}),
    (['-x'], {
        'action': 'store_true',
        'help': 'extract all saved items as .d2i files'}),
    (['-O'], {
        'metavar': 'DEST', 'default': '.',
        'help': 'the output directory when writing d2i files'}),
    (['-v'], {
        'action': 'count', 'default': 0,
        'help': 'increase verbosity. useful for debugging'}),
]

parser = argparse.ArgumentParser(
    prog='pyd2s_stat',
    description='validate and display diablo 2 save file information'
)
for parser_arg in parser_config:
    parser.add_argument(*parser_arg[0], **parser_arg[1])


GLUE = '\n              '


def print_savefile_data(d2s, path):
    '''
    print save file information
    '''
    print(f'''\
[[ Savefile Information ]]
Path        : {path}''')

    if d2s.type == SaveFile.Type.D2S:
        print(f'''\
MagicNumber : {d2s.magic:#08x}
Version     : {d2s.version:#02x}
Timestamp   : {d2s.timestamp} ({datetime.datetime.fromtimestamp(d2s.timestamp)})''')
    else:
        print(f'''\
Header      : {d2s.header}
Version     : {d2s.version:#02x}''')

    if d2s.type == SaveFile.Type.SSS:
        print(f'''\
Shared Gald : {d2s.stored_gold}''')

    return True


def print_character_data(d2s):
    '''
    print character savefile information
    '''
    if d2s.type != SaveFile.Type.D2S:
        return False

    d2s_char = d2s.character

    skill_tree = d2s_char.character_class.skilltree
    skills = (f'{d2s_char.skills[s]:<2} - {s}' for s in skill_tree if d2s_char.skills[s])

    maxgold = d2s_char.stats[Character.StatData.CharacterStat.LEVEL] * 10000

    print(f'''\
[[ Character Information ]]
Name        : {d2s_char.name}
IsExpansion : {d2s_char.is_expansion}
IsHardcore  : {d2s_char.is_hardcore}
HasDied     : {d2s_char.has_died}
Class       : {d2s_char.character_class}
Level       : {d2s_char.stats[Character.StatData.CharacterStat.LEVEL]}

Strength    : {d2s_char.stats[Character.StatData.CharacterStat.STRENGTH]}
Dexterity   : {d2s_char.stats[Character.StatData.CharacterStat.DEXTERITY]}
Vitality    : {d2s_char.stats[Character.StatData.CharacterStat.VITALITY]}
Energy      : {d2s_char.stats[Character.StatData.CharacterStat.ENERGY]}
StatPts     : {d2s_char.stats[Character.StatData.CharacterStat.STATPTS]}
NewSkills   : {d2s_char.stats[Character.StatData.CharacterStat.NEWSKILLS]}

MaxHP       : {int(d2s_char.stats[Character.StatData.CharacterStat.MAXHP] / 256)}
MaxMana     : {int(d2s_char.stats[Character.StatData.CharacterStat.MAXMANA] / 256)}
MaxStamina  : {int(d2s_char.stats[Character.StatData.CharacterStat.MAXSTAMINA] / 256)}

Experience  : {d2s_char.stats[Character.StatData.CharacterStat.EXPERIENCE]}
Gold        : {d2s_char.stats[Character.StatData.CharacterStat.GOLD]:7} / {maxgold:7}
GoldBank    : {d2s_char.stats[Character.StatData.CharacterStat.GOLDBANK]:7} / 2500000

Skill Tree  : {GLUE.join(skills)}''')

    return True


def print_mercenary_data(d2s):
    '''
    print mercenary savefile information
    '''
    if d2s.type != SaveFile.Type.D2S:
        return False

    d2s_merc = d2s.mercenary

    print(f'''\
[[ Mercenary Information ]]
IsDead      : {d2s_merc.is_dead}
ControlSeed : {d2s_merc.control_seed:#x}
Name        : {d2s_merc.name} ({d2s_merc.name_id:#04x})
Type        : {d2s_merc.type} ({d2s_merc.type_id:#04x})
Experience  : {d2s_merc.experience}''')

    return True


def print_quest_act_data(act, d2s_qdata):
    '''
    print quest savefile information for a given act
    '''
    quests = {}
    for act_id in range(1, 6):
        quests[act_id] = map(
            lambda e: format(d2s_qdata[e], '#018b') + f' - {e}',
            filter(lambda e, act_id=act_id: e.act == act_id, Quest))

    print(f'''\
* { act } *
Act I       : { GLUE.join(quests[1]) }
Act II      : { GLUE.join(quests[2]) }
Act III     : { GLUE.join(quests[3]) }
Act IV      : { GLUE.join(quests[4]) }
Act V       : { GLUE.join(quests[5]) }''')


def print_quest_data(d2s):
    '''
    print quest savefile information
    '''
    if d2s.type != SaveFile.Type.D2S:
        return False

    d2s_qdata = d2s.questdata

    print('''\
[[ Quest Information ]]''')

    print_quest_act_data('Normal', d2s_qdata.normal)
    print_quest_act_data('Nightmare', d2s_qdata.nightmare)
    print_quest_act_data('Hell', d2s_qdata.hell)

    return True


def print_waypoint_act_data(act, d2s_wayp):
    '''
    print waypoint savefile information for a given act
    '''
    print(f'''\
* { act } *
Act I       : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(0, 9)) }
Act II      : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(9, 18)) }
Act III     : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(18, 27)) }
Act IV      : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(27, 30)) }
Act V       : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(30, 39)) }''')


def print_waypoint_data(d2s):
    '''
    print waypoint savefile information
    '''
    if d2s.type != SaveFile.Type.D2S:
        return False

    d2s_wayp = d2s.waypointdata

    print('''\
[[ Waypoint Information ]]''')

    print_waypoint_act_data('Normal', d2s_wayp.normal)
    print_waypoint_act_data('Nightmare', d2s_wayp.nightmare)
    print_waypoint_act_data('Hell', d2s_wayp.hell)

    return True


def print_item_data(d2s):
    '''
    print item savefile information
    '''
    if d2s.type == SaveFile.Type.D2I:
        print('''\
[[ Item Information ]]''')
        item = d2s.item
        item.is_identified = True
        print(str(item))
        return True

    if d2s.type in [SaveFile.Type.SSS, SaveFile.Type.D2X]:
        print(f'''\
[[ PlugY Stash Information ]]
Pages       : { len(d2s.pages) }''')
        for (i, page) in enumerate(d2s.pages):
            print(f'''\
  - Page #{i} - '{page.name}' ''')
            for (j, item) in enumerate(page.idata):
                item.is_identified = True
                print(f'  {j:3} ' + '\n      '.join(str(item).splitlines()))
        return True

    d2s_item = d2s.itemdata

    print(f'''\
[[ Player Item Information ]]
Count       : { len(d2s_item.pdata) }''')

    for (i, item) in enumerate(d2s_item.pdata):
        item.is_identified = True
        print(f'{i:3} ' + '\n    '.join(str(item).splitlines()))

    print(f'''
[[ Corpse Item Information ]]
Count       : { len(d2s_item.cdata) }''')

    for (i, item) in enumerate(d2s_item.cdata):
        item.is_identified = True
        print(f'{i:3} ' + '\n    '.join(str(item).splitlines()))

    print(f'''
[[ Mercenary Item Information ]]
Count       : { len(d2s_item.mdata) }''')

    for (i, item) in enumerate(d2s_item.mdata):
        item.is_identified = True
        print(f'{i:3} ' + '\n    '.join(str(item).splitlines()))

    print(f'''
[[ Iron Golem Item Information ]]
Count       : { len(d2s_item.gdata) }''')

    for (i, item) in enumerate(d2s_item.gdata):
        item.is_identified = True
        print(f'{i:3} ' + '\n    '.join(str(item).splitlines()))

    return True


def extract_items(d2s, dest):
    '''
    write test data files for creating test cases with real data
    '''
    items = []
    if d2s.type == SaveFile.Type.D2S:
        items = d2s.itemdata.pdata + d2s.itemdata.cdata + d2s.itemdata.mdata + d2s.itemdata.gdata
    elif d2s.type == SaveFile.Type.D2I:
        items = [d2s.item]
    elif d2s.type in [SaveFile.Type.SSS, SaveFile.Type.D2X]:
        items = [item for page in d2s.pages for item in page.idata]

    for item in items:
        if item.quality >= ItemQuality.MAGICAL:
            item.is_identified = True

        raw_data = item.rawdata

        key = item.name
        if isinstance(item, ExtendedItem):
            key += f' - {item.uid:#010x}'

        path = f'{key}.d2i'
        if dest:
            path = os.path.join(dest, path)

        with open(path, 'wb') as itemfile:
            header = bytearray()
            header.extend('JM'.encode('ascii'))
            header.extend(struct.pack('<L', 0x60))
            assert len(header) == 6
            itemfile.write(header)
            itemfile.write(raw_data)


def pyd2s_stat(argv=None):
    '''
    main entry point
    '''
    args = parser.parse_args(argv)

    logging.basicConfig(level=30 - args.v * 10)

    path = args.filename

    needs_newline = False

    d2s = pyd2s.SaveFile.open(path)

    if args.a or args.s:
        needs_newline = print_savefile_data(d2s, path)

    if args.a or args.c:
        if needs_newline:
            print('')
        needs_newline = print_character_data(d2s)

    if args.a or args.m:
        if needs_newline:
            print('')
        needs_newline = print_mercenary_data(d2s)

    if args.a or args.q:
        if needs_newline:
            print('')
        needs_newline = print_quest_data(d2s)

    if args.a or args.w:
        if needs_newline:
            print('')
        needs_newline = print_waypoint_data(d2s)

    if args.a or args.i:
        if needs_newline:
            print('')
        needs_newline = print_item_data(d2s)

    if args.x:
        extract_items(d2s, args.O)
