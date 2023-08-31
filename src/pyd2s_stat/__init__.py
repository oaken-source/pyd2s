'''
display diablo 2 save file information using pyd2s
'''

import sys
import argparse
import datetime

import pyd2s
from pyd2s.basictypes import CharacterStat, Waypoint

parser = argparse.ArgumentParser(prog='pyd2s_stat',
    description='validate and display diablo 2 save file information')
parser.add_argument('filename')
parser.add_argument('-a', action='store_true',
    help='display all information, equivalent to -scmqwi')
parser.add_argument('-s', action='store_true',
    help='display save file information')
parser.add_argument('-c', action='store_true',
    help='display character information')
parser.add_argument('-m', action='store_true',
    help='display mercenary information')
parser.add_argument('-q', action='store_true',
    help='display quest information')
parser.add_argument('-w', action='store_true',
    help='display waypoint information')
parser.add_argument('-i', action='store_true',
    help='display item information')

def pyd2s_stat(argv=None):
    ''' entry point '''
    args = parser.parse_args(argv)
    path = args.filename

    needs_newline = False

    d2s = pyd2s.D2SaveFile(path)

    if args.a or args.s:
        needs_newline = True
        print(f'''\
[[ Savefile Information ]]
Path        : {path}
MagicNumber : {d2s.magic:#08x}
Version     : {d2s.version:#02x}
Timestamp   : {d2s.timestamp} ({datetime.datetime.fromtimestamp(d2s.timestamp)})''')

    d2s_char = d2s.character

    if args.a or args.c:
        if needs_newline:
            print('')
        needs_newline = True

        glue = '\n              '

        print(f'''\
[[ Character Information ]]
Name        : {d2s_char.name}
IsExpansion : {d2s_char.is_expansion}
IsHardcore  : {d2s_char.is_hardcore}
HasDied     : {d2s_char.has_died}
Class       : {d2s_char.character_class.name}
Level       : {d2s_char.stats[CharacterStat.LEVEL]}

Strength    : {d2s_char.stats[CharacterStat.STRENGTH]}
Dexterity   : {d2s_char.stats[CharacterStat.DEXTERITY]}
Vitality    : {d2s_char.stats[CharacterStat.VITALITY]}
Energy      : {d2s_char.stats[CharacterStat.ENERGY]}
StatPts     : {d2s_char.stats[CharacterStat.STATPTS]}
NewSkills   : {d2s_char.stats[CharacterStat.NEWSKILLS]}

MaxHP       : {d2s_char.stats[CharacterStat.MAXHP]}
MaxMana     : {d2s_char.stats[CharacterStat.MAXMANA]}
MaxStamina  : {d2s_char.stats[CharacterStat.MAXSTAMINA]}

Experience  : {d2s_char.stats[CharacterStat.EXPERIENCE]}
Gold        : {d2s_char.stats[CharacterStat.GOLD]:7} / {d2s_char.stats[CharacterStat.LEVEL] * 10000:7}
GoldBank    : {d2s_char.stats[CharacterStat.GOLDBANK]:7} / 2500000

Skill Tree  : {glue.join(f"{d2s_char.skills[s]:<2} - {s}" for s in d2s_char.character_class.skilltree if d2s_char.skills[s])}''')

    d2s_merc = d2s.mercenary

    if args.a or args.m:
        if needs_newline:
            print('')
        needs_newline = True

        print(f'''\
[[ Mercenary Information ]]
IsDead      : {d2s_merc.is_dead}
ControlSeed : {d2s_merc.control_seed:#x}
NameId      : {d2s_merc.name_id:#04x}
Type        : {d2s_merc.type} ({d2s_merc.type.value:#04x})
Experience  : {d2s_merc.experience}''')

    d2s_qdata = d2s.questdata

    def print_quest_information(act, d2s_qdata):
        print(f'''\
* { act } *
Act I       : { glue.join(format(d2s_qdata[j], '#018b') for j in range(0, 6)) }
Act II      : { glue.join(format(d2s_qdata[j], '#018b') for j in range(6, 12)) }
Act III     : { glue.join(format(d2s_qdata[j], '#018b') for j in range(12, 18)) }
Act IV      : { glue.join(format(d2s_qdata[j], '#018b') for j in range(18, 21)) }
Act V       : { glue.join(format(d2s_qdata[j], '#018b') for j in range(21, 27)) }''')

    if args.a or args.q:
        if needs_newline:
            print('')
        needs_newline = True

        print('''\
[[ Quest Information ]]''')

        print_quest_information('Normal', d2s_qdata.normal)
        print_quest_information('Nightmare', d2s_qdata.nightmare)
        print_quest_information('Hell', d2s_qdata.hell)

    d2s_wayp = d2s.waypointdata

    def print_waypoint_data(act, d2s_wayp):
        print(f'''\
* { act } *
Act I       : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(0, 9)) }
Act II      : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(9, 18)) }
Act III     : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(18, 27)) }
Act IV      : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(27, 30)) }
Act V       : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(30, 39)) }''')

    if args.a or args.w:
        if needs_newline:
            print('')
        needs_newline = True

        print('''\
[[ Waypoint Information ]]''')

        print_waypoint_data('Normal', d2s_wayp.normal)
        print_waypoint_data('Nightmare', d2s_wayp.nightmare)
        print_waypoint_data('Hell', d2s_wayp.hell)

    d2s_item = d2s.itemdata

    if args.a or args.i:
        if needs_newline:
            print('')
        needs_newline = True

        print(f'''\
[[ Player Item Information ]]
Count       : { d2s_item.pcount }''')

        for i in range(d2s_item.pcount):
            print(' - ' + '\n   '.join(str(d2s_item.getpdata(i)).splitlines()))

        print(f'''
[[ Corpse Item Information ]]
Count       : { d2s_item.ccount }''')

        for i in range(d2s_item.ccount):
            print(' - ' + '\n   '.join(str(d2s_item.getcdata(i)).splitlines()))

        print(f'''
[[ Mercenary Item Information ]]
Count       : { d2s_item.mcount }''')

        for i in range(d2s_item.mcount):
            print(' - ' + '\n   '.join(str(d2s_item.getmdata(i)).splitlines()))

        print(f'''
[[ Iron Golem Item Information ]]
Count       : { d2s_item.gcount }''')

        for i in range(d2s_item.gcount):
            print(' - ' + '\n   '.join(str(d2s_item.getgdata(i)).splitlines()))
