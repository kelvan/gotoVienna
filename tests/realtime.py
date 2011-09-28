import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from iTip import iParser

parser = iParser()

class ParseTest(unittest.TestCase):
    
    def test_lines(self):
        lines = parser.lines
        self.assertTrue(type(lines) == dict)
        self.assertTrue(lines)
    
    def test_stations(self):
        lines = parser.lines
        
        s = []
        for line in lines:
            s.append(parser.get_stations(line[0]))
        self.assertTrue(s)

if __name__ == '__main__':
    unittest.main()
