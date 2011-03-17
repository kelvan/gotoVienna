from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2
from datetime import time, datetime
from textwrap import wrap
import settings

class ParserError(Exception):
     def __init__(self, value='', code=0):
         self.value = value
         self.code = code

     def __str__(self):
         return repr(self.value)

class Parser:
    _overview = None
    _details = None
    STATE_ERROR = -1
    STATE_START = 0
    STATE_SEARCH = 1
    STATE_RESULT = 2
    _current_state = 0

    def __init__(self, html):
        self.soup = BeautifulSoup(html)

    def __iter__(self):
        for detail in self.details():
            yield detail
        raise IndexError()

    def _parse_details(self):
        if self._current_state < 0:
            raise ParserError('Unable to parse details while in error state')

        trips = map(lambda x: map(lambda x: {
                                             # TODO kick out wrap
                        'time': map(lambda x: (time(*map(int, x.split(':')))), wrap(x.find('td', {'class': 'col_time'}).text, 5)), # black magic appears
                        'station': map(lambda x: x[2:].strip(),
                                       filter(lambda x: type(x) == NavigableString, x.find('td', {'class': 'col_station'}).contents)), # filter non NaviStrings
                        'info': map(lambda x: x.strip(),
                                    filter(lambda x: type(x) == NavigableString, x.find('td', {'class': 'col_info'}).contents)),
                    }, x.find('tbody').findAll('tr')),
                    self.soup.findAll('div', {'class': 'data_table tourdetail'})) # all routes
        return trips

    @property
    def details(self):
        """returns list of trip details
        [ [ { 'time': [datetime.time, datetime.time] if time else [],
              'station': [u'start', u'end'] if station else [],
              'info': [u'start station' if station else u'details for walking', u'end station' if station else u'walking duration']
            }, ... # next trip step 
          ], ... # next trip possibility
        ]
        """
        if not self._details:
            self._details = self._parse_details()

        return self._details

    def _parse_overview(self):
        def get_tdtext(x, cl):
            return x.find('td', {'class': cl}).text

        def get_change(x):
            y = get_tdtext(x, 'col_change')
            if y:
                return int(y)
            else:
                return 0

        def get_price(x):
            y = get_tdtext(x, 'col_price')
            if y.find(','):
                return float(y.replace(',', '.'))
            else:
                return 0.0

        def get_date(x):
            y = get_tdtext(x, 'col_date')
            if y:
                return datetime.strptime(y, '%d.%m.%Y').date()
            else:
                return None

        # get overview table
        table = self.soup.find('table', {'id': 'tbl_fahrten'})

        # check if there is an overview table
        if table and table.findAll('tr'):
            # get rows
            rows = table.findAll('tr')[1:] # cut off headline
            overview = map(lambda x: {
                               'date': get_date(x),
                               'time': map(lambda x: time(*map(int, x.strip().split(':'))) if x else None, # extract times or set to None if empty
                                           x.find('td', {'class': 'col_time'}).text.split('-')) if x.find('td', {'class': 'col_time'}) else [],
                               'duration': time(*map(int, x.find('td', {'class': 'col_duration'}).text.split(':'))), # grab duration
                               'change': get_change(x),
                               'price': get_price(x),
                           },
                           rows)
        else:
            self._current_state = self.STATE_ERROR
            raise ParserError('Unable to parse details while in error state')

        return overview

    @property
    def overview(self):
        """dict containing
        date: datetime
        time: [time, time]
        duration: time
        change: int
        price: float
        """
        if not self._overview:
            try:
                self._overview = self._parse_overview()
            except AttributeError:
                f = open('DEBUG', 'w')
                f.write(str(self.soup))
                f.close()

        return self._overview

    def _check_request_state(self):
        raise NotImplementedError()

    @property
    def request_state(self):
        return self._current_state


class iParser:
    _stations = {}
    _lines = []

    def __init__(self):
        pass

    def get_stations(self, letter):
        if not self._stations.has_key(letter):
            bs = BeautifulSoup(urllib2.urlopen(settings.stations % letter).read())
            self._stations[letter] = map(lambda x: x['value'], bs.find('select', {'id': 'letter'}).findAll('option'))

        return self._stations[letter]

    def get_lines(self):
        if not self._lines:
            bs = BeautifulSoup(urllib2.urlopen(settings.line_overview).read())
            # get tables
            lines = bs.findAll('table', {'class': 'linie'})
            # cut line parameter out of href
            self._lines = map(lambda x: map(lambda x: x['href'][x['href'].find('=') + 1:], x.findAll('a')), lines)

        return self._lines
