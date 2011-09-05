import unittest
from wlSearch import Search
from datetime import datetime
from parseHtml import Parser, iParser, ParserError
from BeautifulSoup import BeautifulSoup

origin = 'Karlsplatz'
destination = 'Handelskai'
dtime = datetime.now()
dtime = dtime.replace(hour=15, minute=0)
search = Search(origin, destination)
bs = BeautifulSoup(search.get_html(dtime))

class FetchTest(unittest.TestCase):

    def test_overview(self):
        self.assertEquals(1, len(bs.findAll('table', {'id': 'tbl_fahrten'})))

    def test_details(self):
        self.assertTrue(len(bs.findAll('div', {'class': 'data_table tourdetail'})) > 0)

origin = 'Zwicklgasse 1'
destination = 'Himmelstrasse 1'
ot = dt = 'address'
s = Search(origin, destination, origin_type=ot, destination_type=dt)
p = Parser(s.get_html(dtime))

origin = 'Foobar Strasse 123'
destination = 'Bazgasse 321'
s = Search(origin, destination, origin_type=ot, destination_type=dt)
invalid_parser = Parser(s.get_html(dtime))


class ParseTest(unittest.TestCase):

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

    def test_parser_shouldRaiseError(self):
        # TODO Replace with expectedFailure decorator in new python version
        self.assertRaises(ParserError, invalid_parser._parse_overview)

    def test_parser_shouldFindMoreThanOneChange(self):
        self.assertTrue(p.overview[0]['change'] > 0)

    def test_parser_shouldFindPriceGreaterZero(self):
        self.assertTrue(p.overview[0]['price'] > 0.0)

    def test_parser_shouldFindDate(self):
        self.assertTrue(p.overview[0]['date'] == dtime.date())


if __name__ == '__main__':
    unittest.main()
