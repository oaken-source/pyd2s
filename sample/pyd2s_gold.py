import pyd2s

# gold in stash maximize

o_buf = pyd2s.SaveBuffer("C:\\user\\Saved Games\\Diablo II\\player.d2s")
o_char = pyd2s.Character(o_buf)
o_char.goldbank = 2500000
o_buf.flush()

