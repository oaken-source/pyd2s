import pyd2s

# sun gone event flags reset
# This is used when the quest(Act.2 Tainted Sun) is incomplete, dark and inconvenient.

o_buf = pyd2s.SaveBuffer("C:\\user\\Saved Games\\Diablo II\\player.d2s")

o_qdata = pyd2s.QuestData(o_buf)
o_qdata.set_act2_sungone(0, 0)
o_qdata.set_act2_sungone(1, 0)
o_qdata.set_act2_sungone(2, 0)
o_buf.flush()

