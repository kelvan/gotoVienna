# -*- coding: utf-8 -*-

import unittest
from datetime import datetime

from gotovienna.routing import *

dtime = datetime.now()
dtime = dtime.replace(hour=15, minute=0)

origin = u'Börse'.encode('UTF-8')
destination = 'Handelskai'
s = search((origin, 'stop'), (destination, 'stop'), dtime).read()
parser = sParser(s)
p = rParser(s)


originc = 'Simmeri'
destinationc = 'Karlspla'
sc = search((originc, 'stop'), (destinationc, 'stop'), dtime).read()
parserc = sParser(sc)


origina = 'Zwicklgasse 1'
destinationa = 'Himmelstrasse 1'
ot = dt = 'address'


originac = 'Foobar Strasse 123'
destinationac = 'Bazgasse 321'


class SearchTest(unittest.TestCase):

    def test_state(self):
        state = parser.check_page()
        statec = parserc.check_page()
        
        self.assertEqual(PageType.RESULT, state)
        self.assertEqual(PageType.CORRECTION, statec)
        
    def test_correction(self):
        cor = parserc.get_correction()
        s = search((cor[0][0], 'stop'), (cor[1][0], 'stop'), dtime).read()
        parser = sParser(s)
        self.assertEqual(PageType.RESULT, parser.check_page())
    
    def test_overview_shouldFindMultipleItems(self):
        # TODO Replace with assertGreater in new python version
        self.assertTrue(len(p.overview) > 1)

    def test_detail_shouldFindMultipleItems(self):
        # TODO Replace with assertGreater in new python version
        self.assertTrue(len(p.details) > 1)

    def test_detail_shouldFindMultipleStations(self):
        # TODO Replace with assertGreater in new python version
        self.assertTrue(len(p.details[0]) > 1)

    def test_parser_overviewAndDetailsShouldHaveSameLength(self):
        self.assertEqual(len(p.details), len(p.overview))

    def test_parser_shouldFindMoreThanOneChange(self):
        self.assertTrue(p.overview[0]['change'] > 0)

    def test_parser_shouldFindPriceGreaterZero(self):
        self.assertTrue(p.overview[0]['price'] > 0.0)

    def test_parser_shouldFindDate(self):
        self.assertTrue(p.overview[0]['date'] == dtime.date())


if __name__ == '__main__':
    unittest.main()
