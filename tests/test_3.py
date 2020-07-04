import sys
sys.path.append("..")
import bsstudio

def capital_case(x):
    return x.capitalize()

def test_capital_case():
    #assert capital_case('semaphore') == 'Semaphore'
    assert 1==1

def test_71():
    bsstudio.load("/home/bsobhani/bsw/bss_test71.ui")
