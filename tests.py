import unittest
from wlSearch import Search
from datetime import datetime
from parseHtml import Parser, iParser, ParserError
from BeautifulSoup import BeautifulSoup


class FetchTest(unittest.TestCase):

    def setUp(self):
        origin = 'Karlsplatz'
        destination = 'Handelskai'
        dtime = datetime.now()
        dtime = dtime.replace(hour=15, minute=0)
        search = Search(origin, destination)
        self.bs = BeautifulSoup(search.get_html(dtime))

    def test_overview(self):
        self.assertEquals(1, len(self.bs.findAll('table', {'id': 'tbl_fahrten'})))

    def test_details(self):
        self.assertTrue(len(self.bs.findAll('div', {'class': 'data_table tourdetail'})) > 0)


class ParseTest(unittest.TestCase):

    def setUp(self):
        origin = 'Favoritenstrasse 9'
        destination = 'Rathausstrasse 6'
        ot = dt = 'address'
        dtime = datetime.now()
        dtime = dtime.replace(hour=15, minute=0)
        s = Search(origin, destination, origin_type=ot, destination_type=dt)
        self.p = Parser(s.get_html())

        origin = 'Foobar Strasse 123'
        destination = 'Bazgasse 321'
        s = Search(origin, destination, origin_type=ot, destination_type=dt)
        self.invalid_parser = Parser(s.get_html())

    def test_overview_shouldFindMultipleItems(self):
        # TODO Replace with assertGreater in new python version
        self.assertTrue(len(self.p.overview) > 1)

    def test_detail_shouldFindMultipleItems(self):
        # TODO Replace with assertGreater in new python version
        self.assertTrue(len(self.p.details) > 1)

    def test_detail_shouldFindMultipleStations(self):
        # TODO Replace with assertGreater in new python version
        self.assertTrue(len(self.p.details[0]) > 1)

    def test_parser_overviewAndDetailsShouldHaveSameLength(self):
        self.assertEqual(len(self.p.details), len(self.p.overview))

    def test_parser_shouldRaiseError(self):
        # TODO Replace with expectedFailure decorator in new python version
        self.assertRaises(ParserError, self.invalid_parser._parse_overview)


if __name__ == '__main__':
    unittest.main()
