
'''
this module provides classes to manage item of a d2s save
'''

D2_Helms = {
    "cap":"Cap", "xap":"War Hat", "uap":"Shako",
    "skp":"Skull Cap", "xkp":"Sallet", "ukp":"Hydraskull",
    "hlm":"Helm", "xlm":"Casque", "ulm":"Armet",
    "fhl":"Full Helm", "xhl":"Basinet", "uhl":"Giant Conch",
    "ghm":"Great Helm", "xhm":"Winged Helm", "uhm":"Spired Helm",
    "crn":"Crown", "xrn":"Grand Crown", "urn":"Corona",
    "msk":"Mask", "xsk":"Death Mask", "usk":"Demonhead",
    "bhm":"Bone Helm", "xh9":"Grim Helm", "uh9":"Bone Visage"
}

D2_Body_Armors = {
    "qui":"Quilted Armor", "xui":"Ghost Armor", "uui":"Dusk Shroud",
    "lea":"Leather Armor", "xea":"Serpentskin", "uea":"Wyrmhide",
    "hla":"Hard Leather", "xla":"Demonhide Armor", "ula":"Scarab Husk",
    "stu":"Studded Leather", "xtu":"Trellised Armor", "utu":"Wire Fleece",
    "rng":"Ring Mail", "xng":"Linked Mail", "ung":"Diamond Mail",
    "scl":"Scale Mail", "xcl":"Tigulated Mail", "ucl":"Loricated Mail",
    "chn":"Chain Mail", "xhn":"Mesh Armor", "uhn":"Boneweave",
    "brs":"Breast Plate", "xrs":"Cuirass", "urs":"Great Hauberk",
    "spl":"Splint Mail", "xpl":"Russet Armor", "upl":"Balrog Skin",
    "plt":"Plate Mail", "xlt":"Templar Coat", "ult":"Hellforge Plate",
    "fld":"Field Plate", "xld":"Sharktooth", "uld":"Kraken Shell",
    "gth":"Gothic Plate", "xth":"Embossed Plate", "uth":"Lacquered Plate",
    "ful":"Full Plate Mail", "xul":"Chaos Armor", "uul":"Shadow Plate",
    "aar":"Ancient Armor", "xar":"Ornate Armor", "uar":"Sacred Armor",
    "ltp":"Light Plate", "xtp":"Mage Plate", "utp":"Archon Plate"
}

D2_Shields = {
    "buc":"Buckler", "xuc":"Defender", "uuc":"Heater",
    "sml":"Small Shield", "xml":"Round Shield", "uml":"Luna",
    "lrg":"Large Shield", "xrg":"Scutum", "urg":"Hyperion",
    "kit":"Kite Shield", "xit":"Dragon Shield", "uit":"Monarch",
    "tow":"Tower Shield", "xow":"Pavise", "uow":"Aegis",
    "gts":"Gothic Shield", "xts":"Ancient Shield", "uts":"Ward",
    "bsh":"Bone Shield", "xsh":"Grim Shield", "ush":"Troll Nest",
    "spk":"Spiked Shield", "xpk":"Barbed Shield", "upk":"Blade Barrier"
}

D2_Gloves = {
    "lgl":"Leather Gloves", "xlg":"Demonhide Glove", "ulg":"Bramble Mitts",
    "vgl":"Heavy Gloves", "xvg":"Sharkskin Glove", "uvg":"Vampirebone Glo",
    "mgl":"Chain Gloves", "xmg":"Heavy Bracers", "umg":"Vambraces",
    "tgl":"Light Gauntlets", "xtg":"Battle Gauntlet", "utg":"Crusader Gaunt",
    "hgl":"Gauntlets", "xhg":"War Gauntlets", "uhg":"Ogre Gauntlets"
}

D2_Boots = {
    "lbt":"Boots", "xlb":"Demonhide Boots", "ulb":"Wyrmhide Boots",
    "vbt":"Heavy Boots", "xvb":"Sharkskin Boots", "uvb":"Scarabshell Bts",
    "mbt":"Chain Boots", "xmb":"Mesh Boots", "umb":"Boneweave Boots",
    "tbt":"Light Plate", "xtb":"Battle Boots", "utb":"Mirrored Boots",
    "hbt":"Greaves", "xhb":"War Boots", "uhb":"Myrmidon Greave"
}

D2_Belts = {
    "lbl":"Sash", "zlb":"Demonhide Sash", "ulc":"Spiderweb Sash",
    "vbl":"Light Belt", "zvb":"Sharkskin Belt", "uvc":"Vampirefang Blt",
    "mbl":"Belt", "zmb":"Mesh Belt", "umc":"Mithril Coil",
    "tbl":"Heavy Belt", "ztb":"Battle Belt", "utc":"Troll Belt",
    "hbl":"Plated Belt", "zhb":"War Belt", "uhc":"Colossus Girdle"
}

D2_Druid_Pelts = {
    "dr1":"Wolf Head", "dr6":"Alpha Helm", "drb":"Blood Spirit",
    "dr2":"Hawk Helm", "dr7":"Griffon Headress", "drc":"Sun Spirit",
    "dr3":"Antlers", "dr8":"Hunter's Guise", "drd":"Earth Spirit",
    "dr4":"Falcon Mask", "dr9":"Sacred Feathers", "dre":"Sky Spirit",
    "dr5":"Spirit Mask", "dra":"Totemic Mask", "drf":"Dream Spirit"
}

D2_Barbarian_Helms = {
    "ba1":"Jawbone Cap", "ba6":"Jawbone Visor", "bab":"Carnage Helm",
    "ba2":"Fanged Helm", "ba7":"Lion Helm", "bac":"Fury Visor",
    "ba3":"Horned Helm", "ba8":"Rage Mask", "bad":"Destroyer Helm",
    "ba4":"Assualt Helmet", "ba9":"Savage Helmet", "bae":"Conqueror Crown",
    "ba5":"Avenger Guard", "baa":"Slayer Guard", "baf":"Guardian Crown"
}

D2_Necromancer_Shrunken_Heads = {
    "pa1":"Targe", "pa6":"Akaran Targe", "pab":"Sacred Targe",
    "pa2":"Rondache", "pa7":"Akaran Rondache", "pac":"Sacred Rondache",
    "pa3":"Heraldic Shield", "pa8":"Protector Shld", "pad":"Kurast Shield",
    "pa4":"Aerin Shield", "pa9":"Guilded Shield", "pae":"Zakarum Shield",
    "pa5":"Crown Shield", "paa":"Royal Shield", "paf":"Vortex Shield"
}

D2_Paladin_Shields = {
    "ne1":"Preserved Head", "ne6":"Mummified Trphy", "neb":"Minion Skull",
    "ne2":"Zombie Head", "ne7":"Fetish Trophy", "nec":"Hellspawn Skull",
    "ne3":"Unraveller Head", "ne8":"Sexton Trophy", "ned":"Overseer Skull",
    "ne4":"Gargoyle Head", "ne9":"Cantor Trophy", "nee":"Succubae Skull",
    "ne5":"Demon Head", "nea":"Heirophant Trphy", "nef":"Bloodlord Skull"
}

D2_Circlets = {"ci0":"Circlet", "ci1":"Coronet", "ci2":"Tiara", "ci3":"Diadem"}

D2_Armors = [
    D2_Helms, D2_Body_Armors, D2_Shields, D2_Gloves, D2_Boots,
    D2_Belts, D2_Druid_Pelts, D2_Barbarian_Helms, D2_Necromancer_Shrunken_Heads, D2_Paladin_Shields,
    D2_Circlets
]

def isarmors(type):
    val = False
    typea = type[0] + type[1] + type[2]
    for i in range(len(D2_Armors)):
        if typea in D2_Armors[i]:
            val = True
            break
    return val

D2_Axes = {
    "hax":"Hand Axe", "9ha":"Hatchet", "7ha":"Tomahawk",
    "axe":"Axe", "9ax":"Cleaver", "7ax":"Small Crescent",
    "2ax":"Double Axe", "92a":"Twin Axe", "72a":"Ettin Axe",
    "mpi":"Military Pick", "9mp":"Crowbill", "7mp":"War Spike",
    "wax":"War Axe", "9wa":"Naga", "7wa":"Berserker Axe",
    "lax":"Large Axe", "9la":"Military Axe", "7la":"Feral Axe",
    "bax":"Broad Axe", "9ba":"Bearded Axe", "7ba":"Silver Edged Ax",
    "btx":"Battle Axe", "9bt":"Tabar", "7bt":"Decapitator",
    "gax":"Great Axe", "9ga":"Gothic Axe", "7ga":"Champion Axe",
    "gix":"Giant Axe", "9gi":"Ancient Axe", "7gi":"Glorious Axe"
}

D2_Maces = {
    "clb":"Club", "9cl":"Cudgel", "7cl":"Truncheon",
    "spc":"Spiked Club", "9sp":"Barbed Club", "7sp":"Tyrant Club",
    "mac":"Mace", "9ma":"Flanged Mace", "7ma":"Reinforced Mace",
    "mst":"Morning Star", "9mt":"Jagged Star", "7mf":"Devil Star",
    "fla":"Flail", "9fl":"Knout", "7fl":"Scourge",
    "whm":"War Hammer", "9wh":"Battle Hammer", "7wh":"Legendary Mallt",
    "mau":"Maul", "9m9":"War Club", "7m7":"Ogre Maul",
    "gma":"Great Maul", "9gm":"Martel de Fer", "7gm":"Thunder Maul"
}

D2_Swords = {
    "ssd":"Short Swrod", "9ss":"Gladius", "7ss":"Falcata",
    "scm":"Scimitar", "9sm":"Cutlass", "7sm":"Ataghan",
    "sbr":"Saber", "9sb":"Shamshir", "7sb":"Elegant Blade",
    "flc":"Falchion", "9fc":"Tulwar", "7fc":"Hydra Edge",
    "crs":"Crystal Sword", "9cr":"Dimensional Bld", "7cr":"Phase Blade",
    "bsd":"Broad Sword", "9bs":"Battle Sword", "7bs":"Conquest Sword",
    "lsd":"Long Sword", "9ls":"Rune Sword", "7ls":"Cryptic Sword",
    "wsd":"War Sword", "9wd":"Ancient Sword", "7wd":"Mythical Sword",
    "2hs":"Two-handed Swrd", "92h":"Espadon", "72h":"Legend Sword",
    "clm":"Claymore", "9cm":"Dacian Falx", "7cm":"Highland Blade",
    "gis":"Giant Sword", "9gs":"Tusk Sword", "7gs":"Balrog Blade",
    "bsw":"Bastard Sword", "9b9":"Gothic Sword", "7b7":"Champion Sword",
    "flb":"Flamberge", "9fb":"Zweihander", "7fb":"Colossal Sword",
    "gsd":"Great Sword", "9gd":"Executioner Swr", "7gd":"Colossus Blade"
}

D2_Daggers = {
    "dgr":"Dagger", "9dg":"Poignard", "7dg":"Bone Knife",
    "dir":"Dirk", "9di":"Rondel", "7di":"Mithral Point",
    "kri":"Kriss", "9kr":"Cinquedeas", "7kr":"Fanged Knife",
    "bld":"Blade", "9bl":"Stilleto", "7bl":"Legend Spike"
}

D2_Throwing = {
    "tkf":"Throwing Knife", "9tk":"Battle Dart", "7tk":"Flying Knife",
    "tax":"Throwing Axe", "9ta":"Francisca", "7ta":"Flying Axe",
    "bkf":"Balanced Knife", "9bk":"War Dart", "7bk":"Winged Knife",
    "bal":"Balanced Axe", "9b8":"Hurlbat", "7b8":"Winged Axe"
}

D2_Javelins = {
    "jav":"Javelin", "9ja":"War Javelin", "7ja":"Hyperion Javeln",
    "pil":"Pilum", "9pi":"Great Pilum", "7pi":"Stygian Pilum",
    "ssp":"Short Spear", "9s9":"Simbilan", "7s7":"Balrog Spear",
    "glv":"Glaive", "9gl":"Spiculum", "7gl":"Ghost Glaive",
    "tsp":"Throwing Spear", "9ts":"Harpoon", "7ts":"Winged Harpoon"
}

D2_Spears = {
    "spr":"Spear", "9sr":"War Spear", "7sr":"Hyperion Spear",
    "tri":"Trident", "9tr":"Fuscina", "7tr":"Stygian Pike",
    "brn":"Brandistock", "9br":"War Fork", "7br":"Mancatcher",
    "spt":"Spetum", "9st":"Yari", "7st":"Ghost Spear",
    "pik":"Pike", "9p9":"Lance", "7p7":"War Pike"
}

D2_Polearms = {
    "bar":"Bardiche", "9b7":"Lochaber Axe", "7o7":"Ogre Axe",
    "vou":"Voulge", "9vo":"Bill", "7vo":"Colossus Voulge",
    "scy":"Scythe", "9s8":"Battle Scythe", "7s8":"Thresher",
    "pax":"Poleaxe", "9pa":"Partizan", "7pa":"Cryptic Axe",
    "hal":"Halberd", "9h9":"Bec-de-Corbin", "7h7":"Great Poleaxe",
    "wsc":"War Scythe", "9wc":"Grim Scythe", "7wc":"Giant Thresher"
}

D2_Bows = {
    "sbw":"Short Bow", "8sb":"Edge Bow", "6sb":"Spider Bow",
    "hbw":"Hunter's Bow", "8hb":"Razor Bow", "6hb":"Blade Bow",
    "lbw":"Long Bow", "8lb":"Cedar Bow", "6lb":"Shadow Bow",
    "cbw":"Composite Bow", "8cb":"Double Bow", "6cb":"Great Bow",
    "sbb":"Shrt Battle Bow", "8s8":"Short Siege Bow", "6s7":"Diamond Bow",
    "lbb":"Long Battle Bow", "8l8":"Long Siege Bow", "6l7":"Crusader Bow",
    "swb":"Short War Bow", "8sw":"Rune Bow", "6sw":"Ward Bow",
    "lwb":"Long War Bow", "8lw":"Gothic Bow", "6lw":"Hydra Bow"
}

D2_Crossbows = {
    "lxb":"Light Crossbow", "8lx":"Arbalest", "6lx":"Pellet Bow",
    "mxb":"Crossbow", "8mx":"Siege Crossbow", "6mx":"Gorgon Crossbow",
    "hxb":"Heavy Crossbow", "8hx":"Ballista", "6hx":"Colossus x-bow",
    "rxb":"Repeating X-bow", "8rx":"Chu-Ko-Nu", "6rx":"Demon Crossbow"
}

D2_Staves = {
    "sst":"Short Staff", "8ss":"Jo Staff", "6ss":"Walking Stick",
    "lst":"Long Staff", "8ls":"Quarterstaff", "6ls":"Stalagmite",
    "gst":"Gnarled Staff", "8cs":"Cedar Staff", "6cs":"Elder Staff",
    "bst":"Battle Staff", "8bs":"Gothic Staff", "6bs":"Shillelagh",
    "wst":"War Staff", "8ws":"Rune Staff", "6ws":"Archon Staff"
}

D2_Wands = {
    "wnd":"Wand", "9wn":"Burnt Wand", "7wn":"Polished Wand",
    "ywn":"Yew Wand", "9yw":"Petrified Wand", "7yw":"Ghost Wand",
    "bwn":"Bone Wand", "9bw":"Tomb Wand", "7bw":"Lich Wand",
    "gwn":"Grim Wand", "9gw":"Grave Wand", "7gw":"Unearthed Wand"
}

D2_Scepters = {
    "scp":"Sceptre", "9sc":"Rune Sceptre", "7sc":"Mighty Sceptre",
    "gsc":"Grand Sceptre", "9qs":"Holy Water Spri", "7qs":"Seraph Rod",
    "wsp":"War Sceptre", "9ws":"Divine Sceptre", "7ws":"Caduceus"
}

D2_Assassin_Katars = {
    "ktr":"Katar", "9ar":"Quhab", "7ar":"Suwayyah",
    "wrb":"Wrist Blade", "9wb":"Wrist Spike", "7wb":"Wrist Sword",
    "axf":"Hatchet Hands", "9xf":"Fascia", "7xf":"War Fist",
    "ces":"Cestus", "9cs":"Hand Scythe", "7cs":"Battle Cestus",
    "clw":"Claws", "9lw":"Greater Claws", "7lw":"Feral Claws",
    "btl":"Blade Talons", "9hw":"Greater Talons", "7hw":"Runic Talons",
    "skr":"Scissors Katar", "9qr":"Scissors Quhab", "7qr":"Scissors Suwayh"
}

D2_Sorceress_Orbs = {
    "ob1":"Eagle Orb", "ob6":"Glowing Orb", "obb":"Heavenly Stone",
    "ob2":"Sacred Globe", "ob7":"Crystalline Glb", "obc":"Eldritch Orb",
    "ob3":"Smoked Sphere", "ob8":"Cloudy Sphere", "obd":"Demon Heart",
    "ob4":"Clasped Orb", "ob9":"Sparkling Ball", "obe":"Vortex Orb",
    "ob5":"Dragon Stone", "oba":"Swirling Crystl", "obf":"Dimensional Shrd",
}

D2_Amazon_Weapons = {
    "am1":"Stag Bow", "am6":"Ashwood Bow", "amb":"Matriarchal Bow",
    "am2":"Reflex Bow", "am7":"Ceremonial Bow", "amc":"Grnd Matron Bow",
    "am3":"Maiden Spear", "am8":"Ceremonial Spr", "amd":"Matriarchal Spr",
    "am4":"Maiden Pike", "am9":"Ceremonial Pike", "amd":"Matriarchal Pik",
    "am5":"Maiden Javelin", "ama":"Ceremonial Jav", "amf":"Matriarchal Jav"
}
									
D2_Attack_Potions = {
    "gps":"Rancid Gas Pot", "ops":"Oil Potion", "gpm":"Choking Gas Pot",
    "opm":"Exploding Pot", "gpl":"Strangling Gas", "opl":"Fulminating Pot"
}

D2_Weapon_Items = {
    "leg":"Wirt's Leg", "hdm":"Horadric Malus", "msf":"Staff of Kings",
    "hst":"Horadric Staff", "hdm":"Horadric Malus", "msf":"Staff of Kings",
    "g33":"Gidbinn", "qf1":"Khalim's Flail", "qf2":"Khalim's Will", "hfh":"Hellforge Hammr"
}

D2_Weapons = [
    D2_Axes, D2_Maces, D2_Swords, D2_Daggers, D2_Throwing,
    D2_Javelins, D2_Spears, D2_Polearms, D2_Bows, D2_Crossbows,
    D2_Staves, D2_Wands, D2_Scepters, D2_Assassin_Katars, D2_Sorceress_Orbs,
    D2_Amazon_Weapons, D2_Attack_Potions, D2_Weapon_Items
]

def isweapons(type):
    val = False
    typea = type[0] + type[1] + type[2]
    for i in range(len(D2_Weapons)):
        if typea in D2_Weapons[i]:
            val = True
            break
    return val

D2_Items = {
    "bks":"Scroll of Inifuss 1", "bkd":"Scroll of Inifuss 2", "ass":"Book of Skill",
    "box":"Horadric Cube", "tr1":"Horadric Scroll", "ass":"Book of Skill",
    "vip":"Viper Amulet", "xyz":"Potion of Life", "j34":"A Jade Figurine",
    "g34":"The Golden Bird", "bbb":"Lam Esen's Tome", "qey":"Khalim's Eye",
    "qhr":"Khalim's Heart", "qbr":"Khalim's Brain", "mss":"Mephisto's Soulstone",
    "ice":"Malah's Potion", "tr2":"Scroll of Resistance",
    "gcv":"Chipped Amethyst", "gfv":"Flawed Amethyst", "gsv":"Amethyst", "gzv":"Flawless Amethyst", "gpv":"Perfect Amethyst",
    "gcw":"Chipped Diamond", "gfw":"Flawed Diamond", "gsw":"Diamond", "glw":"Flawless Diamond", "gpw":"Perfect Diamond",
    "gcg":"Chipped Emerald", "gfg":"Flawed Emerald", "gsg":"Emerald", "glg":"Flawless Emerald", "gpg":"Perfect Emerald",
    "gcr":"Chipped Ruby", "gfr":"Flawed Ruby", "gsr":"Ruby", "glr":"Flawless Ruby", "gpr":"Perfect Ruby",
    "gcb":"Chipped Saphire", "gfb":"Flawed Saphire", "gsb":"Saphire", "glb":"Flawless Saphire", "gpb":"Perfect Sapphire",
    "gcy":"Chipped Topaz", "gfy":"Flawed Topaz", "gsy":"Topaz", "gly":"Flawless Topaz", "gpy":"Perfect Topaz",
    "skc":"Chipped Skull", "skf":"Flawed Skull", "sku":"Skull", "skl":"Flawless Skull", "skz":"Perfect Skull",
    "r01":"El Rune", "r12":"Sol Rune", "r23":"Mal Rune",
    "r02":"Eld Rune", "r13":"Shael Rune", "r24":"Ist Rune",
    "r03":"Tir Rune", "r14":"Dol Rune", "r25":"Gul Rune",
    "r04":"Nef Rune", "r15":"Hel Rune", "r26":"Vex Rune",
    "r05":"Eth Rune", "r16":"Io Rune", "r27":"Ohm Rune",
    "r06":"Ith Rune", "r17":"Lum Rune", "r28":"Lo Rune",
    "r07":"Tal Rune", "r18":"Ko Rune", "r29":"Sur Rune",
    "r08":"Ral Rune", "r19":"Fal Rune", "r30":"Ber Rune",
    "r09":"Ort Rune", "r20":"Lem Rune", "r31":"Jah Rune",
    "r10":"Thul Rune", "r21":"Pul Rune", "r32":"Cham Rune",
    "r11":"Amn Rune", "r22":"Um Rune", "r33":"Zod Rune",
    "yps":"Antidote Potion", "vps":"Stamina Potion", "wms":"Thawing Potion",
    "hp1":"Minor Healing Potion", "hp2":"Light Healing Potion", "hp3":"Healing Potion", "hp4":"Greater Healing Potion", "hp5":"Super Healing Potion",
    "mp1":"Minor Mana Potion", "mp2":"Light Mana Potion", "mp3":"Mana Potion", "mp4":"Greater Mana Potion", "mp5":"Super Mana Potion",
    "rvs":"Rejuv Potion", "rvl":"Full Rejuv Potion",
    "cm1":"Charm Small", "cm2":"Charm Large", "cm3":"Charm Grand",
    "isc":"Identify Scroll", "tsc":"Town Portal Scroll",
    "ibk":"Tome of Identify", "tbk":"Tome of Town Portal",
    "pk1":"Key of Terror", "pk2":"Key of Hate", "pk3":"Key of Destruction",
    "bey":"Baal's Eye", "dhn":"Diablo's Horn", "mbr":"Mephisto's Brain",
    "bet":"Burning Essence of Terror", "ceh":"Charged Essence of Hatred", "fed":"Festering Essence of Destruction", "tes":"Twisted Essence of Suffering",
    "aqv":"Arrows",
    "cqv":"Bolts",
    "jew":"Jewel",
    "key":"Skeleton Key",
    "amu":"Amulet",
    "gld":"Gold",
    "rin":"Ring",
    "ear":"Ear"
}

D2_Accessories = [
    "jew", "amu", "rin", "cm1", "cm2", "cm3", "vip"
]
								
def isaccessories(type):
    val = False
    typea = type[0] + type[1] + type[2]
    for i in range(len(D2_Accessories)):
        if typea == D2_Accessories[i]:
            val = True
            break
    return val

D2_Countable = [
    "tkf", "9tk", "7tk", "tax", "9ta", "7ta",
    "bkf", "9bk", "7bk", "bal", "9b8", "7b8",
    "jav", "9ja", "7ja", "pil", "9pi", "7pi",
    "ssp", "9s9", "7s7", "glv", "9gl", "7gl",
    "tsp", "9ts", "7ts", "am5", "ama", "amf",
    "gps", "ops", "gpm", "opm", "gpl", "opl",
    "ibk", "tbk", "aqv", "cqv", "key", "gld"
]

def iscountable(type):
    val = False
    typea = type[0] + type[1] + type[2]
    for i in range(len(D2_Countable)):
        if typea == D2_Countable[i]:
            val = True
            break
    return val

D2_Tomes = [
    "ibk", "tbk"
]

def istomes(type):
    val = False
    typea = type[0] + type[1] + type[2]
    for i in range(len(D2_Tomes)):
        if typea == D2_Tomes[i]:
            val = True
            break
    return val

D2_All_Items = [
    D2_Helms, D2_Body_Armors, D2_Shields, D2_Gloves, D2_Boots,
    D2_Belts, D2_Druid_Pelts, D2_Barbarian_Helms, D2_Necromancer_Shrunken_Heads, D2_Paladin_Shields,
    D2_Circlets,
    D2_Axes, D2_Maces, D2_Swords, D2_Daggers, D2_Throwing,
    D2_Javelins, D2_Spears, D2_Polearms, D2_Bows, D2_Crossbows,
    D2_Staves, D2_Wands, D2_Scepters, D2_Assassin_Katars, D2_Sorceress_Orbs,
    D2_Amazon_Weapons, D2_Attack_Potions, D2_Weapon_Items,
    D2_Items
]

def isitems(type):
    val = ""
    typea = type[0] + type[1] + type[2]
    for i in range(len(D2_All_Items)):
        if typea in D2_Items[i]:
            val = D2_Items[i][typea]
            break
    return val

def getitemsname(type):
    val = ""
    typea = type[0] + type[1] + type[2]
    for i in range(len(D2_All_Items)):
        if typea in D2_All_Items[i]:
            val = D2_All_Items[i][typea]
            break
    return val

def getvalfromdata(data, nowbit, bitsize):
    val = 0
    if len(data) * 8 < nowbit + bitsize:
        return val
    mask = 0
    for i in range(nowbit % 8, (nowbit % 8) + bitsize):
        mask |= 1 << i
    d = 0
    if len(data) > (nowbit + bitsize) / 8 + 1:
        for i in range(nowbit / 8, (nowbit + bitsize) / 8 + 1):
            d += data[i] << ((i - nowbit / 8) * 8)
    else:
        for i in range(nowbit / 8, (nowbit + bitsize) / 8):
            d += data[i] << ((i - nowbit / 8) * 8)
    d &= mask
    val = d >> nowbit % 8
    return val

class ItemDetail(object):
    '''
    item detail info
    '''

    def __init__(self, data):
        '''
        constructor - propagate data
        '''
        self._data = data
        self._identified = False
        self._socketed = False
        self._picked = False
        self._ear = False
        self._newbie = False
        self._simple = False
        self._ethereal = False
        self._personalized = False
        self._runeword = False
        self._location = 0
        self._locofequip = 0
        self._column = 0
        self._row = 0
        self._box = 0
        self._type = ""
        self._glued = 0
        self._ear_ownerclass = 0
        self._ear_ownerlevel = 0
        self._ear_ownername = ""
        self._id = 0
        self._ilvl = 0
        self._quality = 0
        self._multipic = False
        self._multipicno = 0
        self._expansion = False
        self._classspecificitem = 0
        self._lowqualitytype = 0
        self._highqualitytype = 0
        self._magicaltype1 = 0
        self._magicaltype2 = 0
        self._settype = 0
        self._rarename1 = 0
        self._rarename2 = 0
        self._raremagicprefix1f = False
        self._raremagicprefix1 = 0
        self._raremagicsuffix1f = False
        self._raremagicsuffix1 = 0
        self._raremagicprefix2f = False
        self._raremagicprefix2 = 0
        self._raremagicsuffix2f = False
        self._raremagicsuffix2 = 0
        self._raremagicprefix3f = False
        self._raremagicprefix3 = 0
        self._raremagicsuffix3f = False
        self._raremagicsuffix3 = 0
        self._unqid = 0
        self._craftname1 = 0
        self._craftname2 = 0
        self._craftmagicprefix1f = False
        self._craftmagicprefix1 = 0
        self._craftmagicsuffix1f = False
        self._craftmagicsuffix1 = 0
        self._craftmagicprefix2f = False
        self._craftmagicprefix2 = 0
        self._craftmagicsuffix2f = False
        self._craftmagicsuffix2 = 0
        self._craftmagicprefix3f = False
        self._craftmagicprefix3 = 0
        self._craftmagicsuffix3f = False
        self._craftmagicsuffix3 = 0
        self._runewordidx = 0
        self._runeworduk = 0
        self._personalizename = ""
        self._uk = 0
        self._defval = 0
        self._maxdur = 0
        self._curdur = 0
        self._socketnum = 0
        self._quantity = 0

        nowbit = 4
        if getvalfromdata(self._data, nowbit, 1):
            self._identified = True
        nowbit = 11
        if getvalfromdata(self._data, nowbit, 1):
            self._socketed = True
        nowbit = 13
        if getvalfromdata(self._data, nowbit, 1):
            self._picked = True
        nowbit = 16
        if getvalfromdata(self._data, nowbit, 1):
            self._ear = True
        nowbit = 17
        if getvalfromdata(self._data, nowbit, 1):
            self._newbie = True
        nowbit = 21
        if getvalfromdata(self._data, nowbit, 1):
            self._simple = True
        nowbit = 22
        if getvalfromdata(self._data, nowbit, 1):
            self._ethereal = True
        nowbit = 24
        if getvalfromdata(self._data, nowbit, 1):
            self._personalized = True
        nowbit = 26
        if getvalfromdata(self._data, nowbit, 1):
            self._runeword = True
        nowbit = 42
        self._location = getvalfromdata(self._data, nowbit, 3)
        nowbit = 45
        self._locofequip = getvalfromdata(self._data, nowbit, 4)
        nowbit = 49
        self._column = getvalfromdata(self._data, nowbit, 4)
        nowbit = 53
        self._row = getvalfromdata(self._data, nowbit, 3)
        nowbit = 57
        self._box = getvalfromdata(self._data, nowbit, 3)
        if not self._ear:
            nowbit = 60
            self._type  = chr(getvalfromdata(self._data, nowbit, 8))
            nowbit += 8
            self._type += chr(getvalfromdata(self._data, nowbit, 8))
            nowbit += 8
            self._type += chr(getvalfromdata(self._data, nowbit, 8))
            nowbit += 8
            self._type += chr(getvalfromdata(self._data, nowbit, 8))
            nowbit = 92
            self._glued = getvalfromdata(self._data, nowbit, 3)
        else:
            nowbit = 60
            self._ear_ownerclass = getvalfromdata(self._data, nowbit, 3)
            nowbit = 63
            self._ear_ownerlevel = getvalfromdata(self._data, nowbit, 7)
            nowbit = 70
            c = getvalfromdata(self._data, nowbit, 7)
            while c:
                self._ear_ownername += chr(c)
                nowbit += 7
                c = getvalfromdata(self._data, nowbit, 7)
        if not self._simple:
            nowbit = 95
            self._id = getvalfromdata(self._data, nowbit, 32)
            nowbit = 127
            self._ilvl = getvalfromdata(self._data, nowbit, 7)
            nowbit = 134
            self._quality = getvalfromdata(self._data, nowbit, 4)
            nowbit += 4
            if isaccessories(self._type):
                if getvalfromdata(self._data, nowbit, 1):
                    self._multipic = True
                nowbit += 1
                if self._multipic:
                    self._multipicno = getvalfromdata(self._data, nowbit, 3)
                    nowbit += 3
            else:
                self._uk = getvalfromdata(self._data, nowbit, 1)
                nowbit += 1
            if getvalfromdata(self._data, nowbit, 1):
                self._expansion = True
            nowbit += 1
            if self._expansion:
                self._classspecificitem = getvalfromdata(self._data, nowbit, 11)
                nowbit += 11
            if self._quality == 1:
                self._lowqualitytype = getvalfromdata(self._data, nowbit, 3)
                nowbit += 3
            elif self._quality == 3:
                self._highqualitytype = getvalfromdata(self._data, nowbit, 3)
                nowbit += 3
            elif self._quality == 4:
                self._magicaltype1 = getvalfromdata(self._data, nowbit, 11)
                nowbit += 11
                self._magicaltype2 = getvalfromdata(self._data, nowbit, 11)
                nowbit += 11
            elif self._quality == 5:
                self._settype = getvalfromdata(self._data, nowbit, 12)
                nowbit += 12
            elif self._quality == 6:
                self._rarename1 = getvalfromdata(self._data, nowbit, 8)
                nowbit += 8
                self._rarename2 = getvalfromdata(self._data, nowbit, 8)
                nowbit += 8
                if getvalfromdata(self._data, nowbit, 1):
                    self._raremagicprefix1f = True
                nowbit += 1
                if self._raremagicprefix1f:
                    self._raremagicprefix1 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._raremagicsuffix1f = True
                nowbit += 1
                if self._raremagicsuffix1f:
                    self._raremagicsuffix1 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._raremagicprefix2f = True
                nowbit += 1
                if self._raremagicprefix2f:
                    self._raremagicprefix2 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._raremagicsuffix2f = True
                nowbit += 1
                if self._raremagicsuffix2f:
                    self._raremagicsuffix2 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._raremagicprefix3f = True
                nowbit += 1
                if self._raremagicprefix3f:
                    self._raremagicprefix3 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._raremagicsuffix3f = True
                nowbit += 1
                if self._raremagicsuffix3f:
                    self._raremagicsuffix3 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
            elif self._quality == 7:
                self._unqid = getvalfromdata(self._data, nowbit, 12)
                nowbit += 12
            elif self._quality == 8:
                self._craftname1 = getvalfromdata(self._data, nowbit, 8)
                nowbit += 8
                self._craftname2 = getvalfromdata(self._data, nowbit, 8)
                nowbit += 8
                if getvalfromdata(self._data, nowbit, 1):
                    self._craftmagicprefix1f = True
                nowbit += 1
                if self._craftmagicprefix1f:
                    self._craftmagicprefix1 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._craftmagicsuffix1f = True
                nowbit += 1
                if self._craftmagicsuffix1f:
                    self._craftmagicsuffix1 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._craftmagicprefix2f = True
                nowbit += 1
                if self._craftmagicprefix2f:
                    self._craftmagicprefix2 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._craftmagicsuffix2f = True
                nowbit += 1
                if self._craftmagicsuffix2f:
                    self._craftmagicsuffix2 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._craftmagicprefix3f = True
                nowbit += 1
                if self._craftmagicprefix3f:
                    self._craftmagicprefix3 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
                if getvalfromdata(self._data, nowbit, 1):
                    self._craftmagicsuffix3f = True
                nowbit += 1
                if self._craftmagicsuffix3f:
                    self._craftmagicsuffix3 = getvalfromdata(self._data, nowbit, 11)
                    nowbit += 11
            if self._runeword:
                self._runewordidx = getvalfromdata(self._data, nowbit, 12)
                nowbit += 12
                self._runeworduk = getvalfromdata(self._data, nowbit, 4)
                nowbit += 4
            if self._personalized:
                for i in range(15):
                    c = getvalfromdata(self._data, nowbit, 7)
                    nowbit += 7
                    if c:
                        self._personalizename += chr(c)
                    else:
                        break
            self._uk = getvalfromdata(self._data, nowbit, 1)
            nowbit += 1
            if isarmors(self._type):
                self._defval = getvalfromdata(self._data, nowbit, 10) - 10
                nowbit += 10
                self._uk = getvalfromdata(self._data, nowbit, 1)
                nowbit += 1
            if isarmors(self._type) or isweapons(self._type):
                self._maxdur = getvalfromdata(self._data, nowbit, 8)
                nowbit += 8
                self._curdur = getvalfromdata(self._data, nowbit, 8)
                nowbit += 8
                if self._socketed and not iscountable(self._type):
                    self._uk = getvalfromdata(self._data, nowbit, 1)
                    nowbit += 1
                    self._socketnum = getvalfromdata(self._data, nowbit, 4)
                    nowbit += 4
            if istomes(self._type):
                self._uk = getvalfromdata(self._data, nowbit, 5)
                nowbit += 5
            if iscountable(self._type):
                self._quantity = getvalfromdata(self._data, nowbit, 9)
                nowbit += 9

    @property
    def getdata(self):
        '''
        item data
        '''
        return self._data

    @property
    def isidentified(self):
        '''
        item is identified
        '''
        return self._identified

    @property
    def issocketed(self):
        '''
        item is socketed
        '''
        return self._socketed

    @property
    def ispicked(self):
        '''
        item is picked up since the last time
        '''
        return self._picked

    @property
    def isear(self):
        '''
        item is player ear
        '''
        return self._ear

    @property
    def isnewbie(self):
        '''
        item is newbie
        '''
        return self._newbie

    @property
    def issimple(self):
        '''
        item is simple
        '''
        return self._simple

    @property
    def isethereal(self):
        '''
        item is ethereal
        '''
        return self._ethereal

    @property
    def ispersonalized(self):
        '''
        item is personalized
        '''
        return self._personalized

    @property
    def isruneword(self):
        '''
        item has been given a rune word
        '''
        return self._runeword

    @property
    def getlocation(self):
        '''
        item location
        '''
        return self._location

    @property
    def getlocofequip(self):
        '''
        item location of equipped
        '''
        return self._locofequip

    @property
    def getcolumn(self):
        '''
        item column
        '''
        return self._column

    @property
    def getrow(self):
        '''
        item row
        '''
        return self._row

    @property
    def getbox(self):
        '''
        where box item is in
        '''
        return self._box

    @property
    def gettype(self):
        '''
        item type
        '''
        return self._type

    @property
    def getglued(self):
        '''
        number of glued to item 
        '''
        return self._glued

    @property
    def getearownerclass(self):
        '''
        owner class of item ear
        '''
        return self._ear_ownerclass

    @property
    def getearownerlevel(self):
        '''
        owner level of item ear
        '''
        return self._ear_ownerlevel

    @property
    def getearownername(self):
        '''
        owner name of item ear
        '''
        return self._ear_ownername

    @property
    def getid(self):
        '''
        item id
        '''
        return self._id

    @property
    def getilvl(self):
        '''
        item level
        '''
        return self._ilvl

    @property
    def getquality(self):
        '''
        item quality
        '''
        return self._quality

    @property
    def ismultipic(self):
        '''
        item has multiple picture
        '''
        return self._multipic

    @property
    def getmultipicno(self):
        '''
        item's multiple picture number
        '''
        return self._multipicno

    @property
    def isexpansion(self):
        '''
        Expantion Set items
        '''
        return self._expansion

    @property
    def getclassspecificitem(self):
        '''
        class specific item
        '''
        return self._classspecificitem

    @property
    def getlowqualitytype(self):
        '''
        item low quality type
        '''
        return self._lowqualitytype

    @property
    def gethighqualitytype(self):
        '''
        item high quality type
        '''
        return self._highqualitytype

    @property
    def getmagicaltype1(self):
        '''
        item magical type 1
        '''
        return self._magicaltype1

    @property
    def getmagicaltype2(self):
        '''
        item magical type 2
        '''
        return self._magicaltype2

    @property
    def getsettype(self):
        '''
        item set type
        '''
        return self._settype

    @property
    def getrarename1(self):
        '''
        item rare name 1
        '''
        return self._rarename1

    @property
    def getrarename2(self):
        '''
        item rare name 2
        '''
        return self._rarename2

    @property
    def israremagicprefix1(self):
        '''
        Is item rare 1st prefix be
        '''
        return self._raremagicprefix1f

    @property
    def getraremagicprefix1(self):
        '''
        item rare 1st prefix
        '''
        return self._raremagicprefix1

    @property
    def israremagicsuffix1(self):
        '''
        Is item rare 1st suffix be
        '''
        return self._raremagicsuffix1f

    @property
    def getraremagicsuffix1(self):
        '''
        item rare 1st suffix
        '''
        return self._raremagicsuffix1

    @property
    def israremagicprefix2(self):
        '''
        Is item rare 2nd prefix be
        '''
        return self._raremagicprefix2f

    @property
    def getraremagicprefix2(self):
        '''
        item rare 2nd prefix
        '''
        return self._raremagicprefix2

    @property
    def israremagicsuffix2(self):
        '''
        Is item rare 2nd suffix be
        '''
        return self._raremagicsuffix2f

    @property
    def getraremagicsuffix2(self):
        '''
        item rare 2nd suffix
        '''
        return self._raremagicsuffix2

    @property
    def israremagicprefix3(self):
        '''
        Is item rare 3rd prefix be
        '''
        return self._raremagicprefix3f

    @property
    def getraremagicprefix3(self):
        '''
        item rare 3rd prefix
        '''
        return self._raremagicprefix3

    @property
    def israremagicsuffix3(self):
        '''
        Is item rare 3rd suffix be
        '''
        return self._raremagicsuffix3f

    @property
    def getraremagicsuffix3(self):
        '''
        item rare 3rd suffix
        '''
        return self._raremagicsuffix3

    @property
    def getunqid(self):
        '''
        item unique id
        '''
        return self._unqid

    @property
    def getcraftname1(self):
        '''
        item craft name 1
        '''
        return self._craftname1

    @property
    def getcraftname2(self):
        '''
        item craft name 2
        '''
        return self._craftname2

    @property
    def iscraftmagicprefix1(self):
        '''
        Is item craft 1st prefix be
        '''
        return self._craftmagicprefix1f

    @property
    def getcraftmagicprefix1(self):
        '''
        item craft 1st prefix
        '''
        return self._craftmagicprefix1

    @property
    def iscraftmagicsuffix1(self):
        '''
        Is item craft 1st suffix be
        '''
        return self._craftmagicsuffix1f

    @property
    def getcraftmagicsuffix1(self):
        '''
        item craft 1st suffix
        '''
        return self._craftmagicsuffix1

    @property
    def iscraftmagicprefix2(self):
        '''
        Is item craft 2nd prefix be
        '''
        return self._craftmagicprefix2f

    @property
    def getcraftmagicprefix2(self):
        '''
        item craft 2nd prefix
        '''
        return self._craftmagicprefix2

    @property
    def iscraftmagicsuffix2(self):
        '''
        Is item craft 2nd suffix be
        '''
        return self._craftmagicsuffix2f

    @property
    def getcraftmagicsuffix2(self):
        '''
        item craft 2nd suffix
        '''
        return self._craftmagicsuffix2

    @property
    def iscraftmagicprefix3(self):
        '''
        Is item craft 3rd prefix be
        '''
        return self._craftmagicprefix3f

    @property
    def getcraftmagicprefix3(self):
        '''
        item craft 3rd prefix
        '''
        return self._craftmagicprefix3

    @property
    def iscraftmagicsuffix3(self):
        '''
        Is item craft 3rd suffix be
        '''
        return self._craftmagicsuffix3f

    @property
    def getcraftmagicsuffix3(self):
        '''
        item craft 3rd suffix
        '''
        return self._craftmagicsuffix3

    @property
    def getrunewordidx(self):
        '''
        item rune word index
        '''
        return self._runewordidx

    @property
    def getpersonalizename(self):
        '''
        item personalized name
        '''
        return self._personalizename

    @property
    def getdefval(self):
        '''
        item defense value
        '''
        return self._defval

    @property
    def getmaxdur(self):
        '''
        item max durability
        '''
        return self._maxdur

    @property
    def getcurdur(self):
        '''
        item current durability
        '''
        return self._curdur

    @property
    def getsocketnum(self):
        '''
        item socket number
        '''
        return self._socketnum

    @property
    def getquantity(self):
        '''
        item quantity
        '''
        return self._quantity

class Item(object):
    '''
    save data related to item
    '''

    def __init__(self, buffer):
        '''
        constructor - propagate buffer
        '''
        self._buffer = buffer
        self._pcount = 0
        self._pcountondata = 0
        self._mcount = 0
        self._mcountondata = 0
        self._pdata = []
        self._mdata = []

        loc = 840    # about
	start = True
        first = True
        player = True
        onedata = []
        while loc < len(self._buffer):
            if self._buffer[loc] == ord("J") and self._buffer[loc + 1] == ord("M"):
                if start:
                    start = False
                else:
                    if len(onedata) == 2:
                        if not self._pcountondata:
                            self._pcountondata = (onedata[1] << 8) + onedata[0]
                        elif not self._mcountondata:
                            self._mcountondata = (onedata[1] << 8) + onedata[0]
                    elif len(onedata) == 4:
                        if not self._pcountondata:
                            pass
                        if not self._mcountondata:
                            player = False
                    elif len(onedata) > 4:
                        if player:
                            if len(onedata) > 4:
                                self._pdata.append(ItemDetail(onedata))
                        else:
                            if len(onedata) > 4:
                                self._mdata.append(ItemDetail(onedata))
                        if player:
                            self._pcount += 1
                        else:
                            self._mcount += 1
                onedata = []
                loc += 2
            else:
                if not start:
                    onedata.append(self._buffer[loc])
                loc += 1
        if len(onedata):
            if player:
                if len(onedata) > 4:
                    self._pdata.append(ItemDetail(onedata))
            else:
                if len(onedata) > 4:
                    self._mdata.append(ItemDetail(onedata))
            if onedata[0] != 0x00 or onedata[1] != 0x00 or onedata[2] != 0x6A:
                if player:
                    self._pcount += 1
                else:
                    self._mcount += 1

    @property
    def pcount(self):
        '''
        player item count
        '''
        return self._pcount

    @property
    def pcountondata(self):
        '''
        player item count (on data)
        '''
        return self._pcountondata

    def getpdata(self, index):
        '''
        Get player item data
        '''
        if(index >= len(self._pdata)):
            return []
        else:
            return self._pdata[index]

    @property
    def mcount(self):
        '''
        mercenary item count
        '''
        return self._mcount

    @property
    def mcountondata(self):
        '''
        mercenary item count (on data)
        '''
        return self._mcountondata

    def getmdata(self, index):
        '''
        Get mercenary item data
        '''
        if(index >= len(self._mdata)):
            return []
        else:
            return self._mdata[index]

