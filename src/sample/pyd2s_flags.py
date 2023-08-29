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
if d2s_qdata[Quest.TOOLS_OF_THE_TRADE] & 0x1:
    d2s_qdata[Quest.TOOLS_OF_THE_TRADE] = d2s_qdata[Quest.TOOLS_OF_THE_TRADE] & ~0x3 | 0x2

# reset completion on Cowlevel
d2s_qdata[Quest.THE_SEARCH_FOR_CAIN] = d2s_qdata[Quest.THE_SEARCH_FOR_CAIN] & ~(0x1<<10)

# reset completion on Larzuk's socket reward
d2s_qdata[Quest.SIEGE_OF_HARROGATH] = d2s_qdata[Quest.SIEGE_OF_HARROGATH] & ~(0x1<<5)

# reset completion on Anya's personalization reward
if d2s_qdata[Quest.BETRAYAL_OF_HARROGATH] & 0x1:
    d2s_qdata[Quest.BETRAYAL_OF_HARROGATH] = d2s_qdata[Quest.BETRAYAL_OF_HARROGATH] & ~0x3 | 0x2

# save data back to disk
d2s.flush()
