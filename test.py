import epics
import time

def cache_length():
	return sum([len(val.access_callbacks) for key, val in epics.pv._PVcache_.items()])

#sig = EpicsSignal('XF:21IDA-OP{Mir:1-Ax:4_Pitch}Mtr.RBV')
for i in range(10):
	sig = EpicsSignal('XF:21IDA-OP{Mir:1-Ax:4_Pitch}Mtr.RBV')
	sig.destroy()
	
	print(cache_length())
	time.sleep(1)
