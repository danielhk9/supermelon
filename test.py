import pytest



def fun(x):
    return x+5

def test_nme():
    assert fun(3) == 8