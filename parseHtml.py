from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2
from datetime import time, datetime
from textwrap import wrap


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
        trips = map(lambda x: map(lambda x: {
                        'time': map(lambda x: (time(*map(lambda x: int(x), x.split(':')))), wrap(x.find('td', {'class': 'col_time'}).text, 5)), # black magic appears
                        'station': map(lambda x: x[2:].strip(),
                                       filter(lambda x: type(x) == NavigableString, x.find('td', {'class': 'col_station'}).contents)), # filter non NaviStrings
                        'info': map(lambda x: x.strip(),
                                    filter(lambda x: type(x) == NavigableString, x.find('td', {'class': 'col_info'}).contents)),
                    }, x.find('tbody').findAll('tr')),
                    self.soup.findAll('div', {'class': 'data_table tourdetail'})) # all routes
        return trips

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
                           'date': datetime.strptime(x.find('td', {'class': 'col_date'}).text, '%d.%m.%Y') # grab date
                                       if x.find('td', {'class': 'col_date'}).text else None, # if date is empty set to None
                           'time': map(lambda x: time(*map(lambda x: int(x), x.split(':'))) if x else None, # extract times or set to None if empty
                                       x.find('td', {'class': 'col_time'}).text.split('  - ')),
                           'duration': time(*map(lambda x: int(x), x.find('td', {'class': 'col_duration'}).text.split(':'))), # grab duration
                           'change': int(x.find('td', {'class': 'col_change'}).text) # grab changes
                                       if x.find('td', {'class': 'col_change'}).text else 0, # if change is empty set to 0
                           'price': float(x.find('td', {'class': 'col_price'}).text.replace(',', '.')) # grab price
                                       if x.find('td', {'class': 'col_price'}).text.find(',') >= 0 else 0.0, # if price is empty set to 0.0
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
