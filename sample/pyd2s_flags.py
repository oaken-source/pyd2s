'''
sample usage of pyd2s that resets quest rewards
'''

import sys

import pyd2s
from pyd2s.basictypes import Quest


# open a d2s file
d2s = pyd2s.D2SaveFile(sys.argv[1])
d2s_qdata = d2s.questdata.normal

# reset completion on Charsi's imbue reward
if d2s_qdata[Quest.ToolsOfTheTrade] & 0x1:
    d2s_qdata[Quest.ToolsOfTheTrade] = d2s_qdata[Quest.ToolsOfTheTrade] & ~0x3 | 0x2

# reset completion on Cowlevel
d2s_qdata[Quest.TheSearchForCain] = d2s_qdata[Quest.TheSearchForCain] & ~(0x1<<10)

# reset completion on Larzuk's socket reward
d2s_qdata[Quest.SiegeOfHarrogath] = d2s_qdata[Quest.SiegeOfHarrogath] & ~(0x1<<5)

# reset completion on Anya's personalization reward
if d2s_qdata[Quest.BetrayalOfHarrogath] & 0x1:
    d2s_qdata[Quest.BetrayalOfHarrogath] = d2s_qdata[Quest.BetrayalOfHarrogath] & ~0x3 | 0x2

# save data back to disk
d2s.flush()
