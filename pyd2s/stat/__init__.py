'''
display diablo 2 save file information using pyd2s
'''

import sys
import argparse
import datetime

import pyd2s

parser = argparse.ArgumentParser(prog='pyd2s_stat',
    description='display diablo 2 save file information')
parser.add_argument('filename')

def pyd2s_stat(argv=None):
    ''' entry point '''
    args = parser.parse_args(argv)
    path = args.filename

    d2s = pyd2s.D2SaveFile(path)
    print(f'''\
[[ Savefile Information ]]
Path        : {path}
MagicNumber : {d2s.magic:#08x}
Version     : {d2s.version:#02x}
Timestamp   : {d2s.timestamp} ({datetime.datetime.fromtimestamp(d2s.timestamp)})''')

    d2s_char = pyd2s.Character(d2s._buffer)
    print(f'''
[[ Character Information ]]
Name        : {d2s_char.name}
IsExpansion : {d2s_char.is_expansion}
IsHardcore  : {d2s_char.is_hardcore}
HasDied     : {d2s_char.has_died}
Class       : {d2s_char.character_class.name}
Level       : {d2s_char.level}

Strength    : {d2s_char.strength}
Dexterity   : {d2s_char.dexterity}
Vitality    : {d2s_char.vitality}
Energy      : {d2s_char.energy}
StatPts     : {d2s_char.statpts}
NewSkills   : {d2s_char.newskills}

MaxHP       : {d2s_char.maxhp}
MaxMana     : {d2s_char.maxmana}
MaxStamina  : {d2s_char.maxstamina}

Experience  : {d2s_char.experience}
Gold        : {d2s_char.gold}
GoldBank    : {d2s_char.goldbank}''')

    d2s_merc = pyd2s.Mercenary(d2s._buffer)
    print(f'''
[[ Mercenary Information ]]
IsDead      : {d2s_merc.is_dead}
ControlSeed : {d2s_merc.control_seed:#x}
NameId      : {d2s_merc.name_id:#04x}
Type        : {d2s_merc.type} ({d2s_merc.type_id:#04x})
Experience  : {d2s_merc.experience}''')

    d2s_qdata = pyd2s.QuestData(d2s._buffer)

    print(f'''
[[ Quest Information ]]''')

    def print_quest_information(act, d2s_qdata):

        glue = '\n              '
        print(f'''\
* { act } *
Act I       : { glue.join(format(d2s_qdata[j], '#018b') for j in range(0, 6)) }
Act II      : { glue.join(format(d2s_qdata[j], '#018b') for j in range(6, 12)) }
Act III     : { glue.join(format(d2s_qdata[j], '#018b') for j in range(12, 18)) }
Act IV      : { glue.join(format(d2s_qdata[j], '#018b') for j in range(18, 21)) }
Act V       : { glue.join(format(d2s_qdata[j], '#018b') for j in range(21, 27)) }''')

    print_quest_information('Normal', d2s_qdata.normal)
    print_quest_information('Nightmare', d2s_qdata.nightmare)
    print_quest_information('Hell', d2s_qdata.hell)

    d2s_wayp = pyd2s.WaypointData(d2s._buffer)
    print(f'''
[[ Waypoint Information ]]''')

    def print_waypoint_data(act, d2s_wayp):
        print(f'''\
* { act } *
Act I       : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(0, 9)) }
Act II      : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(9, 18)) }
Act III     : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(18, 27)) }
Act IV      : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(27, 30)) }
Act V       : { '/'.join('o' if d2s_wayp[j] else 'x' for j in range(30, 39)) }''')

    print_waypoint_data('Normal', d2s_wayp.normal)
    print_waypoint_data('Nightmare', d2s_wayp.nightmare)
    print_waypoint_data('Hell', d2s_wayp.hell)

    d2s_item = pyd2s.ItemData(d2s._buffer)
    print(f'''
[[ Player Item Information ]]
Count       : { d2s_item.pcount } (on data: {d2s_item.pcountondata})
''')

    def print_item(data):
        temp = ""
        temp += "("
        if len(data) > 6:
            temp += "C{} R{} ".format((data[6] & 0x1E) >> 1, (data[6] & 0xE0) >> 5)
        if len(data) > 5:
            val = (data[5] & 0x1C) >> 2
            if val == 2:
                temp += "Belt"
            elif val == 4:
                temp += "Cursor"
            elif val == 6:
                temp += "Socket"
        if len(data) > 6:
            if (data[5] & 0x1C) >> 2 == 1:
                val = ((data[5] & 0xE0) >> 5) + ((data[6] & 0x1) << 3)
                if val == 1:
                    temp += "(E)Heads"
                elif val == 2:
                    temp += "(E)Neck"
                elif val == 3:
                    temp += "(E)Torso"
                elif val == 4:
                    temp += "(E)RHand"
                elif val == 5:
                    temp += "(E)LHand"
                elif val == 6:
                    temp += "(E)RFinger"
                elif val == 7:
                    temp += "(E)LFinger"
                elif val == 8:
                    temp += "(E)Waist"
                elif val == 9:
                    temp += "(E)Feet"
                elif val == 10:
                    temp += "(E)Hands"
                elif val == 11:
                    temp += "(E)ARHand"
                elif val == 12:
                    temp += "(E)ALHand"
        if len(data) > 7:
            if (data[5] & 0x1C) >> 2 == 0:
                val = (data[7] & 0x0E) >> 1
                if val == 0:
                    temp += "NotHere"
                elif val == 1:
                    temp += "Inventory"
                elif val == 4:
                    temp += "Cube"
                elif val == 5:
                    temp += "Stash"
        temp += ") "
        if len(data) > 10:
            temp2 = [((data[ 7] & 0xF0) >> 4) + ((data[ 8] & 0x0F) << 4), ((data[ 8] & 0xF0) >> 4) + ((data[ 9] & 0x0F) << 4),
                     ((data[ 9] & 0xF0) >> 4) + ((data[10] & 0x0F) << 4), ((data[10] & 0xF0) >> 4) + ((data[11] & 0x0F) << 4)]
            temp += "{:02X} {:02X} {:02X} {:02X} ({}) ".format(temp2[0], temp2[1], temp2[2], temp2[3], chr(temp2[0]) + chr(temp2[1]) + chr(temp2[2]) + chr(temp2[3]))
        if len(data) > 0:
            if data[0] & 0x10 == 0:
                temp += "NonIdentified "
        if len(data) > 2:
            if data[2] & 0x01:
                temp += "Ear "
            if data[2] & 0x02:
                temp += "Newbie "
            if data[2] & 0x40:
                temp += "Ethereal "
        if len(data) > 3:
            if data[3] & 0x01:
                temp += "Personalized "
            if data[3] & 0x04:
                temp += "Runeword "
        if len(data) > 11:
            val = (data[11] & 0x70) >> 4
            if data[1] & 0x08 and val > 0:
                temp += "Socketed({}) ".format(val)
        if len(data) > 2:
            if data[2] & 0x20 == 0:    # not simple
                if len(data) > 16:
                    val = ((data[15] & 0x80) >> 7) + ((data[16] & 0x3F) << 1)
                    temp += "ilvl({}) ".format(val)
        print("item {}".format(i) + " : " + temp)
        temp = ""
        for j in range(len(data)):
            temp += "{:02X} ".format(data[j])
        print("item {}".format(i) + " : " + temp)

    for i in range(d2s_item.pcount):
        print_item(d2s_item.getpdata(i))

    print(f'''
[[ Mercenary Item Information ]]
Count       : { d2s_item.mcount } (on data: {d2s_item.mcountondata})
''')

    for i in range(d2s_item.mcount):
        print_item(d2s_item.getmdata(i))
