import pyd2s

# forge and bonus event flags reset

o_buf = pyd2s.SaveBuffer("C:\\user\\Saved Games\\Diablo II\\player.d2s")

o_qdata = pyd2s.QuestData(o_buf)
o_qdata.set_act1_resetstatus(0, 0)
o_qdata.set_act1_resetstatus(1, 0)
o_qdata.set_act1_resetstatus(2, 0)
o_qdata.set_act1_forge(0, 0)
o_qdata.set_act1_forge(1, 0)
o_qdata.set_act1_forge(2, 0)
o_qdata.set_act1_cowlevel(0, 0)
o_qdata.set_act1_cowlevel(1, 0)
o_qdata.set_act1_cowlevel(2, 0)
o_qdata.set_act5_socket(0, 0)
o_qdata.set_act5_socket(1, 0)
o_qdata.set_act5_socket(2, 0)
o_qdata.set_act5_personalize(0, 0)
o_qdata.set_act5_personalize(1, 0)
o_qdata.set_act5_personalize(2, 0)
o_buf.flush()

