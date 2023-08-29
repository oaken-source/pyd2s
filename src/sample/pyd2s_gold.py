'''
sample usage of pyd2s that increases the amount of gold to max
'''

import sys

import pyd2s


# open a d2s file
d2s = pyd2s.D2SaveFile(sys.argv[1])
d2s_char = d2s.character

# set the gold in the bank to max
d2s_char.goldbank = 2500000

# save data back to disk
d2s.flush()
