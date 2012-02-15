from nose.tools import assert_true, assert_false
import sys
from os import path

DATA = path.join(path.dirname(__file__), 'data')
HASHFILENAME = 'hashtestfile'

with open(path.join(DATA, HASHFILENAME + '.md5')) as f:
    HASH = f.read()

sys.path.insert(0, path.dirname(path.dirname(__file__)))
from gotovienna.update import compare_hash

def test_hash_equal():
    assert_true(compare_hash(HASH, path.join(DATA, HASHFILENAME)))

def test_hash_not_equal():
    assert_false(compare_hash('GG' + HASH[2:], path.join(DATA, HASHFILENAME)))

