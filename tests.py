import unittest
from wlSearch import Search
from datetime import datetime
from BeautifulSoup import BeautifulSoup


class FetchTests(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
