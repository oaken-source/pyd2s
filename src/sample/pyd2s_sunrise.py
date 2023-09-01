'''
sample usage of pyd2s that clears the darkness in act 2
'''

import sys

import pyd2s
from pyd2s.basictypes import Quest


# open a d2s file
d2s = pyd2s.D2SaveFile(sys.argv[1])
d2s_qdata = d2s.questdata.normal

# regress the quest to clear the darkness
if not d2s_qdata[Quest.TAINTED_SUN] & (1 << 10):
    d2s_qdata[Quest.TAINTED_SUN] = d2s_qdata[Quest.TAINTED_SUN] & ~(1 << 2)

# save data back to disk
d2s.flush()
