from BeautifulSoup import BeautifulSoup
import urllib2
from datetime import time, datetime


class Parser:
    _overview = None
    _details = None

    def __init__(self, html):
        self.soup = BeautifulSoup(html)

    def __iter__(self):
        for detail in self.details():
            yield detail
        raise IndexError()

    def _parse_details(self):
        return self.soup.findAll('div', {'class': 'data_table tourdetail'})

    @property
    def details(self):
        if not self._details:
            self._details = self._parse_details()

        return self._details

    def _parse_overview(self):
        """
        Returns dict containing
        date: datetime
        time: [time, time]
        duration: time
        change: int
        price: float
        """
        # get overview table
        table = self.soup.find('table', {'id': 'tbl_fahrten'})
        # get rows
        rows = table.findAll('tr')[1:]
        overview = map(lambda x: {
                       'date': datetime.strptime(x.find('td', {'class': 'col_date'}).text, '%d.%m.%Y'), # grab date
                       'time': map(lambda x: time(*map(lambda x: int(x), x.split(':'))), x.find('td', {'class': 'col_time'}).text.split('  - ')), # extract times
                       'duration': time(*map(lambda x: int(x), x.find('td', {'class': 'col_duration'}).text.split(':'))), # grab duration
                       'change': int(x.find('td', {'class': 'col_change'}).text), # grab changes
                       'price': float(x.find('td', {'class': 'col_price'}).text.replace(',', '.')) # grab price
                       },
            rows)

        return overview

    @property
    def overview(self):
        if not self._overview:
            self._overview = self._parse_overview()

        return self._overview


class iTipParser:

    def __init__(self):
        raise NotImplementedError
