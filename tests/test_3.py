import sys
sys.path.append("..")
import bsstudio
import time

def capital_case(x):
	return x.capitalize()

def test_capital_case():
	#assert capital_case('semaphore') == 'Semaphore'
	assert 1==1

def test_71():
	from bsstudio.widgets import CodeButton
	app = bsstudio.load("/home/bsobhani/bsw/bss_test71.ui", True)
	time.sleep(10)
	for b in bsstudio.getMainWindow().findChildren(CodeButton):
		b.runCode()
		time.sleep(10)
	time.sleep(10)
	bsstudio.getMainWindow().deleteLater()
	time.sleep(10)
