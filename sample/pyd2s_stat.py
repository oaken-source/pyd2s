import pyd2s

# informations of savefile

path = "C:\\user\\Saved Games\\Diablo II\\player.d2s"
o_d2s = pyd2s.D2SaveFile(path)
o_d2s_buf = pyd2s.SaveBuffer(path)
o_d2s_char = pyd2s.Character(o_d2s_buf)
o_d2s_merc = pyd2s.Mercenary(o_d2s_buf)
o_d2s_qdata = pyd2s.QuestData(o_d2s_buf)
o_d2s_wayp = pyd2s.WaypointData(o_d2s_buf)
o_d2s_item = pyd2s.Item(o_d2s_buf)

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
print("Class       : " + str(o_d2s_char.character_class))
print("Level       : " + str(o_d2s_char.level))
print("")
print("Strength  : " + str(o_d2s_char.strength))
print("Dexterity : " + str(o_d2s_char.dexterity))
print("Vitality  : " + str(o_d2s_char.vitality))
print("Energy    : " + str(o_d2s_char.energy))
print("StatPts   : " + str(o_d2s_char.statpts))
print("")
print("NewSkills : " + str(o_d2s_char.newskills))
print("")
print("MaxHP   : " + str(o_d2s_char.maxhp))
print("MaxMP   : " + str(o_d2s_char.maxmana))
print("Stamina : " + str(o_d2s_char.maxstamina))
print("")
print("Experience : " + str(o_d2s_char.experience))
print("Gold       : " + str(o_d2s_char.gold))
print("GoldBank   : " + str(o_d2s_char.goldbank))
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
print("Count          : " + str(o_d2s_item.pcount))
print("Count(on data) : " + str(o_d2s_item.pcountondata))
print("")

for i in range(o_d2s_item.pcount):
    o_itemdata = o_d2s_item.getpdata(i)
    temp = "item{}".format(i) + ": "
    temp += "("
    temp += "C{} R{}".format(o_itemdata.getcolumn, o_itemdata.getrow)
    if o_itemdata.getlocation == 0:
        if o_itemdata.getbox == 0:
            temp += " (NotHere)"
        elif o_itemdata.getbox == 1:
            temp += " Inventory"
        elif o_itemdata.getbox == 4:
            temp += " Cube"
        elif o_itemdata.getbox == 5:
            temp += " Stash"
    elif o_itemdata.getlocation == 1:
        temp += " Equipped"
        if o_itemdata.getlocofequip == 1:
            temp += " Head"
        elif o_itemdata.getlocofequip == 2:
            temp += " Neck"
        elif o_itemdata.getlocofequip == 3:
            temp += " Torso"
        elif o_itemdata.getlocofequip == 4:
            temp += " RHand"
        elif o_itemdata.getlocofequip == 5:
            temp += " LHand"
        elif o_itemdata.getlocofequip == 6:
            temp += " RFinger"
        elif o_itemdata.getlocofequip == 7:
            temp += " LFinger"
        elif o_itemdata.getlocofequip == 8:
            temp += " Waist"
        elif o_itemdata.getlocofequip == 9:
            temp += " Feet"
        elif o_itemdata.getlocofequip == 10:
            temp += " Hands"
        elif o_itemdata.getlocofequip == 11:
            temp += " ARHand"
        elif o_itemdata.getlocofequip == 12:
            temp += " ALHand"
    elif o_itemdata.getlocation == 2:
        temp += " Belt"
    elif o_itemdata.getlocation == 4:
        temp += " Cursor"
    elif o_itemdata.getlocation == 5:
        temp += " Socketed"
    temp += ") "
    print(temp)
    temp = "  "
    if o_itemdata.getquality == 1:
        temp += "[LQ] "
    elif o_itemdata.getquality == 3:
        temp += "[HQ] "
    elif o_itemdata.getquality == 4:
        temp += "\x1b[1;34m[Magic]\x1b[0m "
    elif o_itemdata.getquality == 5:
        temp += "\x1b[1;32m[Set]\x1b[0m "
    elif o_itemdata.getquality == 6:
        temp += "\x1b[1;33m[Rare]\x1b[0m "
    elif o_itemdata.getquality == 7:
        temp += "\x1b[1;33m[Unique]\x1b[0m "
    elif o_itemdata.getquality == 8:
        temp += "\x1b[1;31m[Crafted]\x1b[0m "
    temp += pyd2s.getitemsname(o_itemdata.gettype) + "(" + o_itemdata.gettype + ")"
    if not o_itemdata.isidentified:
        temp += " NotIdentified"
    if o_itemdata.issocketed:
        temp += " Socketed"
    if o_itemdata.isethereal:
        temp += " Ethereal"
    if o_itemdata.ispersonalized:
        temp += " Personalized(" + o_itemdata.getpersonalizename + ")"
    if o_itemdata.isruneword:
        temp += " RuneWord"
    if o_itemdata.getglued != 0:
        temp += " Glued({})".format(o_itemdata.getglued)
    if not o_itemdata.issimple:
        temp += " ID(0x{:08X})".format(o_itemdata.getid)
        temp += " ilvl({})".format(o_itemdata.getilvl)
    if pyd2s.isarmors(o_itemdata.gettype):
        temp += " Def({})".format(o_itemdata.getdefval)
    if (pyd2s.isarmors(o_itemdata.gettype) or pyd2s.isweapons(o_itemdata.gettype)):
        temp += " Durability({}/{})".format(o_itemdata.getcurdur, o_itemdata.getmaxdur)
        if o_itemdata.issocketed:
            temp += " Sockets({})".format(o_itemdata.getsocketnum)
    print(temp)
print("")

print("[[ Mercenary Item information ]]")
print("Count          : " + str(o_d2s_item.mcount))
print("Count(on data) : " + str(o_d2s_item.mcountondata))
print("")

for i in range(o_d2s_item.mcount):
    o_itemdata = o_d2s_item.getmdata(i)
    temp = "item{}".format(i) + ": "
    temp += "("
    temp += "C{} R{}".format(o_itemdata.getcolumn, o_itemdata.getrow)
    if o_itemdata.getlocation == 0:
        if o_itemdata.getbox == 0:
            temp += " (NotHere)"
        elif o_itemdata.getbox == 1:
            temp += " Inventory"
        elif o_itemdata.getbox == 4:
            temp += " Cube"
        elif o_itemdata.getbox == 5:
            temp += " Stash"
    elif o_itemdata.getlocation == 1:
        temp += " Equipped"
        if o_itemdata.getlocofequip == 1:
            temp += " Head"
        elif o_itemdata.getlocofequip == 2:
            temp += " Neck"
        elif o_itemdata.getlocofequip == 3:
            temp += " Torso"
        elif o_itemdata.getlocofequip == 4:
            temp += " RHand"
        elif o_itemdata.getlocofequip == 5:
            temp += " LHand"
        elif o_itemdata.getlocofequip == 6:
            temp += " RFinger"
        elif o_itemdata.getlocofequip == 7:
            temp += " LFinger"
        elif o_itemdata.getlocofequip == 8:
            temp += " Waist"
        elif o_itemdata.getlocofequip == 9:
            temp += " Feet"
        elif o_itemdata.getlocofequip == 10:
            temp += " Hands"
        elif o_itemdata.getlocofequip == 11:
            temp += " ARHand"
        elif o_itemdata.getlocofequip == 12:
            temp += " ALHand"
    elif o_itemdata.getlocation == 2:
        temp += " Belt"
    elif o_itemdata.getlocation == 4:
        temp += " Cursor"
    elif o_itemdata.getlocation == 5:
        temp += " Socketed"
    temp += ") "
    print(temp)
    temp = "  "
    if o_itemdata.getquality == 1:
        temp += "[LQ] "
    elif o_itemdata.getquality == 3:
        temp += "[HQ] "
    elif o_itemdata.getquality == 4:
        temp += "\x1b[1;34m[Magic]\x1b[0m "
    elif o_itemdata.getquality == 5:
        temp += "\x1b[1;32m[Set]\x1b[0m "
    elif o_itemdata.getquality == 6:
        temp += "\x1b[1;33m[Rare]\x1b[0m "
    elif o_itemdata.getquality == 7:
        temp += "\x1b[1;33m[Unique]\x1b[0m "
    elif o_itemdata.getquality == 8:
        temp += "\x1b[1;31m[Crafted]\x1b[0m "
    temp += pyd2s.getitemsname(o_itemdata.gettype) + "(" + o_itemdata.gettype + ")"
    if not o_itemdata.isidentified:
        temp += " NotIdentified"
    if o_itemdata.issocketed:
        temp += " Socketed"
    if o_itemdata.isethereal:
        temp += " Ethereal"
    if o_itemdata.ispersonalized:
        temp += " Personalized(" + o_itemdata.getpersonalizename + ")"
    if o_itemdata.isruneword:
        temp += " RuneWord"
    if o_itemdata.getglued != 0:
        temp += " Glued({})".format(o_itemdata.getglued)
    if not o_itemdata.issimple:
        temp += " ID(0x{:08X})".format(o_itemdata.getid)
        temp += " ilvl({})".format(o_itemdata.getilvl)
    if pyd2s.isarmors(o_itemdata.gettype):
        temp += " Def({})".format(o_itemdata.getdefval)
    if (pyd2s.isarmors(o_itemdata.gettype) or pyd2s.isweapons(o_itemdata.gettype)):
        temp += " Durability({}/{})".format(o_itemdata.getcurdur, o_itemdata.getmaxdur)
        if o_itemdata.issocketed:
            temp += " Sockets({})".format(o_itemdata.getsocketnum)
    print(temp)


