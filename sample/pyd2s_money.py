import pyd2s

o_buf = pyd2s.SaveBuffer("/home/domi/.wine/drive_c/users/domi/Saved Games/Diablo II/catman.d2s")
o_char = pyd2s.Character(o_buf)
o_char.goldbank = 2500000
o_buf.flush()

