import pyd2s
import platform
import pkgutil
import importlib

# colorama module load, if exist
colorama = None
for i in pkgutil.iter_modules():
    if platform.python_version_tuple()[0] == "2":
        c = i[1]
    elif platform.python_version_tuple()[0] == "3":
        c = i.name
    if c == "colorama":
        colorama = importlib.import_module("colorama")
        break

# informations of savefile

path = "C:\\user\\Saved Games\\Diablo II\\player.d2s"
o_d2s = pyd2s.D2SaveFile(path)
o_d2s_buf = pyd2s.SaveBuffer(path)
o_d2s_char = pyd2s.Character(o_d2s_buf)
o_d2s_merc = pyd2s.Mercenary(o_d2s_buf)
o_d2s_qdata = pyd2s.QuestData(o_d2s_buf)
o_d2s_wayp = pyd2s.WaypointData(o_d2s_buf)
o_d2s_item = pyd2s.Item(o_d2s_buf)
o_d2s_skill = pyd2s.Skill(o_d2s_buf)


def printitem(index, item):
    if item == None:
        return

    if 0:
        data = item.getdata
        temp = ""
        for j in range(len(data)):
            temp += "{:02X} ".format(data[j])
        print(temp)
    temp = "item{}".format(index) + ": "
    temp += "("
    temp += "C{} R{}".format(item.getcolumn, item.getrow)
    if item.getlocation == 0:
        if item.getbox == 0:
            temp += " (NotHere)"
        elif item.getbox == 1:
            temp += " Inventory"
        elif item.getbox == 4:
            temp += " Cube"
        elif item.getbox == 5:
            temp += " Stash"
    elif item.getlocation == 1:
        temp += " Equipped"
        if item.getlocofequip == 1:
            temp += " Head"
        elif item.getlocofequip == 2:
            temp += " Neck"
        elif item.getlocofequip == 3:
            temp += " Torso"
        elif item.getlocofequip == 4:
            temp += " RHand"
        elif item.getlocofequip == 5:
            temp += " LHand"
        elif item.getlocofequip == 6:
            temp += " RFinger"
        elif item.getlocofequip == 7:
            temp += " LFinger"
        elif item.getlocofequip == 8:
            temp += " Waist"
        elif item.getlocofequip == 9:
            temp += " Feet"
        elif item.getlocofequip == 10:
            temp += " Hands"
        elif item.getlocofequip == 11:
            temp += " ARHand"
        elif item.getlocofequip == 12:
            temp += " ALHand"
    elif item.getlocation == 2:
        temp += " Belt"
    elif item.getlocation == 4:
        temp += " Cursor"
    elif item.getlocation == 5:
        temp += " Socketed"
    temp += ") "
    print(temp)
    temp = "  "
    if item.getquality == 1:
        if colorama:
            temp += colorama.Fore.WHITE + "[LQ] " + colorama.Fore.RESET
        else:
            temp += "[LQ] "
    elif item.getquality == 3:
        temp += "[HQ] "
    elif item.getquality == 4:
        if colorama:
            temp += colorama.Fore.LIGHTBLUE_EX + "[Magic] " + colorama.Fore.RESET
        else:
            temp += "[Magic] "
    elif item.getquality == 5:
        if colorama:
            temp += colorama.Fore.LIGHTGREEN_EX + "[Set] " + colorama.Fore.RESET
        else:
            temp += "[Set] "
    elif item.getquality == 6:
        if colorama:
            temp += colorama.Fore.LIGHTYELLOW_EX + "[Rare] " + colorama.Fore.RESET
        else:
            temp += "[Rare] "
    elif item.getquality == 7:
        if colorama:
            temp += colorama.Fore.LIGHTYELLOW_EX + "[Unique] " + colorama.Fore.RESET
        else:
            temp += "[Unique] "
    elif item.getquality == 8:
        if colorama:
            temp += colorama.Fore.LIGHTRED_EX + "[Crafted] " + colorama.Fore.RESET
        else:
            temp += "[Crafted] "
    temp += item.getname + "(" + item.gettype + ")"
    if not item.isidentified:
        temp += " NotIdentified"
    if item.issocketed:
        temp += " Socketed"
    if item.isethereal:
        if colorama:
            temp += colorama.Fore.WHITE + " Ethereal" + colorama.Fore.RESET
        else:
            temp += " Ethereal"
    if item.ispersonalized:
        if colorama:
            temp += colorama.Fore.LIGHTRED_EX + " Personalized(" + item.getpersonalizename + ")" + colorama.Fore.RESET
        else:
            temp += " Personalized(" + item.getpersonalizename + ")"
    if item.isruneword:
        if colorama:
            temp += colorama.Fore.LIGHTYELLOW_EX + " RuneWord" + colorama.Fore.RESET
        else:
            temp += " RuneWord"
    if item.getglued != 0:
        temp += " Glued({})".format(item.getglued)
    if not item.issimple:
        temp += " ID(0x{:08X})".format(item.getid)
        temp += " ilvl({})".format(item.getilvl)
    if item.isarmors:
        temp += " Def({})".format(item.getdefval)
    if (item.isarmors or item.isweapons):
        temp += " Durability({}/{})".format(item.getcurdur, item.getmaxdur)
        if item.issocketed:
            if colorama:
                temp += colorama.Fore.WHITE + " Sockets({})".format(item.getsocketnum) + colorama.Fore.RESET
            else:
                temp += " Sockets({})".format(item.getsocketnum)
    if item.iscountable:
        temp += " Quantity({})".format(item.getquantity)
    print(temp)


def printitemlist(itemlist):
    if itemlist == None:
        return

    print("Count          : " + str(itemlist.count))
    print("Count(on data) : " + str(itemlist.countondata))
    print("")

    for i in range(itemlist.count):
        printitem(i, itemlist.getitem(i))
    print("")


print("[[ Savefile information ]]")
print("Path     : " + o_d2s_buf.path)
print("Magicnum : 0x{:08X}".format(o_d2s.magic))
print("Version  : 0x{:02X}".format(o_d2s.version))
print("Timestump: {} seconds".format(o_d2s.timestamp))
print("")

print("[[ Charctor information ]]")
print("Name        : " + o_d2s_char.name)
if o_d2s_char.is_expansion:
    temp = "Yes"
else:
    temp = "No"
print("IsExpantion : " + temp)
if o_d2s_char.is_hardcore:
    if(o_d2s_char.has_died):
        temp = "Yes(died)"
    else:
        temp = "Yes(alive)"
else:
    if(o_d2s_char.has_died):
        temp = "No(died)"
    else:
        temp = "No(alive)"
print("IsHardCore  : " + temp)
if o_d2s_char.character_class == pyd2s.CharacterClass.Amazon:
    c = "Amazon"
elif o_d2s_char.character_class == pyd2s.CharacterClass.Sorceress:
    c = "Sorceress"
elif o_d2s_char.character_class == pyd2s.CharacterClass.Necromancer:
    c = "Necromancer"
elif o_d2s_char.character_class == pyd2s.CharacterClass.Paladin:
    c = "Paladin"
elif o_d2s_char.character_class == pyd2s.CharacterClass.Barbarian:
    c = "Barbarian"
elif o_d2s_char.character_class == pyd2s.CharacterClass.Druid:
    c = "Druid"
elif o_d2s_char.character_class == pyd2s.CharacterClass.Assassin:
    c = "Assassin"
print("Class       : " + c)
print("Level       : " + str(o_d2s_char.level))
print("")
print("Strength  : " + str(o_d2s_char.strength))
print("Dexterity : " + str(o_d2s_char.dexterity))
print("Vitality  : " + str(o_d2s_char.vitality))
print("Energy    : " + str(o_d2s_char.energy))
print("StatPts   : " + str(o_d2s_char.statpts))
print("")
print("MaxHP   : " + str(o_d2s_char.maxhp))
print("MaxMP   : " + str(o_d2s_char.maxmana))
print("Stamina : " + str(o_d2s_char.maxstamina))
print("")
print("Experience : " + str(o_d2s_char.experience))
print("Gold       : " + str(o_d2s_char.gold))
print("GoldBank   : " + str(o_d2s_char.goldbank))
print("")

print("[[ Skill information ]]")
if o_d2s_char.character_class == pyd2s.CharacterClass.Amazon:
    cc = 0
elif o_d2s_char.character_class == pyd2s.CharacterClass.Sorceress:
    cc = 1
elif o_d2s_char.character_class == pyd2s.CharacterClass.Necromancer:
    cc = 2
elif o_d2s_char.character_class == pyd2s.CharacterClass.Paladin:
    cc = 3
elif o_d2s_char.character_class == pyd2s.CharacterClass.Barbarian:
    cc = 4
elif o_d2s_char.character_class == pyd2s.CharacterClass.Druid:
    cc = 5
elif o_d2s_char.character_class == pyd2s.CharacterClass.Assassin:
    cc = 6
j = 0
for i in range(30):
    if j < len(o_d2s_skill.getskillname(i)):
        j = len(o_d2s_skill.getskillname(i))
for i in range(30):
    idx = pyd2s.D2_SkillsOrder[cc][i]
    temp = o_d2s_skill.getskillname(idx)
    for m in range(j - len(o_d2s_skill.getskillname(idx))):
        temp += " "
    if colorama:
        if o_d2s_skill.getskillpoints(idx) >= 20:
            temp += " : " + colorama.Fore.LIGHTRED_EX + "{}".format(o_d2s_skill.getskillpoints(idx)) + colorama.Fore.RESET
        else:
            temp += " : {}".format(o_d2s_skill.getskillpoints(idx))
    else:
        temp += " : {}".format(o_d2s_skill.getskillpoints(idx))
    print(temp)
    if (i + 1) % 10 == 0:
        print("")
print("NewSkills : " + str(o_d2s_char.newskills))
print("")

print("[[ Mercenary information ]]")
if o_d2s_merc.is_dead:
    temp = "Dead"
else:
    temp = "Alive"
print("IsDead      : " + temp)
print("ControlSeed : 0x{:X}".format(o_d2s_merc.control_seed))
print("NameId      : 0x{:X}".format(o_d2s_merc.name_id))
if o_d2s_merc.type == 1:
    temp = "Act.1"
elif o_d2s_merc.type == 2:
    temp = "Act.2"
elif o_d2s_merc.type == 3:
    temp = "Act.3"
elif o_d2s_merc.type == 4:
    temp = "Act.5"
else:
    temp = "(illegal)"
print("Type        : " + temp)
print("")

print("[[ Quest information ]]")
for i in range(3):
    if i == 0:
        print("* Normal *")
    if i == 1:
        print("* Nightmare *")
    if i == 2:
        print("* Hell *")
    if o_d2s_qdata.get_act1_resetstatus(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.1 Reset status And skills : " + temp)
    if o_d2s_qdata.get_act1_forge(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.1 Forge                   : " + temp)
    if o_d2s_qdata.get_act1_cowlevel(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.1 Cow Level               : " + temp)
    if o_d2s_qdata.get_act2_radament(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.2 Radament quest          : " + temp)
    if o_d2s_qdata.get_act3_goldenbird(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.3 Golden Bird quest       : " + temp)
    if o_d2s_qdata.get_act3_lamesen(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.3 Lam Esen quest          : " + temp)
    if o_d2s_qdata.get_act4_izual(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.4 Izual quest             : " + temp)
    if o_d2s_qdata.get_act5_socket(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.5 Socket                  : " + temp)
    if o_d2s_qdata.get_act5_runesset(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.5 Runes set               : " + temp)
    if o_d2s_qdata.get_act5_scrollofregist(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.5 Scroll of regist        : " + temp)
    if o_d2s_qdata.get_act5_personalize(i):
        temp = "x"
    else:
        temp = "o"
    print("Act.5 Personalize             : " + temp)
print("")

print("[[ Waypoint information ]]")
for i in range(3):
    if i == 0:
        print("* Normal *")
    if i == 1:
        print("* Nightmare *")
    if i == 2:
        print("* Hell *")
    temp = "Act.1 : "
    if i == 0:
        for j in range(8):
            if o_d2s_wayp.normal[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.normal[8]:
            temp += "o"
        else:
            temp += "x"
    if i == 1:
        for j in range(8):
            if o_d2s_wayp.nightmare[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.nightmare[8]:
            temp += "o"
        else:
            temp += "x"
    if i == 2:
        for j in range(8):
            if o_d2s_wayp.hell[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.hell[8]:
            temp += "o"
        else:
            temp += "x"
    print(temp)
    temp = "Act.2 : "
    if i == 0:
        for j in range(9, 17):
            if o_d2s_wayp.normal[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.normal[17]:
            temp += "o"
        else:
            temp += "x"
    if i == 1:
        for j in range(9, 17):
            if o_d2s_wayp.nightmare[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.nightmare[17]:
            temp += "o"
        else:
            temp += "x"
    if i == 2:
        for j in range(9, 17):
            if o_d2s_wayp.hell[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.hell[17]:
            temp += "o"
        else:
            temp += "x"
    print(temp)
    temp = "Act.3 : "
    if i == 0:
        for j in range(18, 26):
            if o_d2s_wayp.normal[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.normal[26]:
            temp += "o"
        else:
            temp += "x"
    if i == 1:
        for j in range(18, 26):
            if o_d2s_wayp.nightmare[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.nightmare[26]:
            temp += "o"
        else:
            temp += "x"
    if i == 2:
        for j in range(18, 26):
            if o_d2s_wayp.hell[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.hell[26]:
            temp += "o"
        else:
            temp += "x"
    print(temp)
    temp = "Act.4 : "
    if i == 0:
        for j in range(27, 29):
            if o_d2s_wayp.normal[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.normal[29]:
            temp += "o"
        else:
            temp += "x"
    if i == 1:
        for j in range(27, 29):
            if o_d2s_wayp.nightmare[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.nightmare[29]:
            temp += "o"
        else:
            temp += "x"
    if i == 2:
        for j in range(27, 29):
            if o_d2s_wayp.hell[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.hell[29]:
            temp += "o"
        else:
            temp += "x"
    print(temp)
    temp = "Act.5 : "
    if i == 0:
        for j in range(30, 38):
            if o_d2s_wayp.normal[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.normal[38]:
            temp += "o"
        else:
            temp += "x"
    if i == 1:
        for j in range(30, 38):
            if o_d2s_wayp.nightmare[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.nightmare[38]:
            temp += "o"
        else:
            temp += "x"
    if i == 2:
        for j in range(30, 38):
            if o_d2s_wayp.hell[j]:
                temp += "o/"
            else:
                temp += "x/"
        if o_d2s_wayp.hell[38]:
            temp += "o"
        else:
            temp += "x"
    print(temp)
print("")

print("[[ Player Item information ]]")
printitemlist(o_d2s_item.pitemlist)

if o_d2s_item.ccount > 0:
    if o_d2s_item.ccount == 1:
        print("[[ Corpse Item information ]]")
        temp = "Corpse ID: "
        data = o_d2s_item.getcid(0)
        for i in range(len(data)):
            temp += "{:02X} ".format(data[i])
        print(temp)
        itemlist = o_d2s_item.getcitemlist(0)
        printitemlist(itemlist)
    else:
        for i in range(o_d2s_item.ccount):
            print("[[ Corpse Item information {} ]]".format(i))
            printitemlist(o_d2s_item.getcitemlist(i))

if o_d2s_item.mitemlist:
    print("[[ Mercenary Item information ]]")
    printitemlist(o_d2s_item.mitemlist)

if o_d2s_item.hasgolem:
    print("[[ Golem Item information ]]")
    printitem(0, o_d2s_item.golemitem)

