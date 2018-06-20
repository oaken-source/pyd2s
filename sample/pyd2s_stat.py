import pyd2s

# informations of savefile

path = "/home/domi/.wine/drive_c/users/domi/Saved Games/Diablo II/catman.d2s"
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
		if o_d2s_wayp.hell[28]:
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
    temp = ""
    data = o_d2s_item.getpdata(i)
    for j in range(len(data)):
        temp += "{:02X} ".format(data[j])
    print("item{}".format(i) + " : " + temp)
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
    print(temp)
print("")

print("[[ Mercenary Item information ]]")
print("Count          : " + str(o_d2s_item.mcount))
print("Count(on data) : " + str(o_d2s_item.mcountondata))
print("")

for i in range(o_d2s_item.mcount):
    temp = ""
    data = o_d2s_item.getmdata(i)
    for j in range(len(data)):
        temp += "{:02X} ".format(data[j])
    print("item{}".format(i) + " : " + temp)
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
            if val == 1:
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
    print(temp)


