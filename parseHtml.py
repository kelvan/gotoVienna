from BeautifulSoup import BeautifulSoup, NavigableString
import urllib2
from datetime import time, datetime
from textwrap import wrap
import settings
import wlSearch

class ParserError(Exception):
     def __init__(self, value='', code=0):
         self.value = value
         self.code = code

     def __str__(self):
         return repr(self.value)

class Parser:
    STATE_ERROR = -1
    STATE_START, STATE_SEARCH, STATE_RESULT = range(3)

    def __init__(self, html):
        self.soup = BeautifulSoup(html)
        self._overview = None
        self._details = None
        self._current_state = 0

    @classmethod
    def get_tdtext(cls, x, cl):
            return x.find('td', {'class': cl}).text
    
    @classmethod
    def get_change(cls, x):
        y = Parser.get_tdtext(x, 'col_change')
        if y:
            return int(y)
        else:
            return 0

    @classmethod
    def get_price(cls, x):
        y = Parser.get_tdtext(x, 'col_price')
        if y.find(','):
            return float(y.replace(',', '.'))
        else:
            return 0.0

    @classmethod
    def get_date(cls, x):
        y = Parser.get_tdtext(x, 'col_date')
        if y:
            return datetime.strptime(y, '%d.%m.%Y').date()
        else:
            return None
        
    @classmethod
    def get_time(cls, x):
        y = Parser.get_tdtext(x, 'col_time')
        if y:
            if (y.find("-") > 0):
                return map(lambda z: time(*map(int, z.split(':'))), y.split('-'))
            else:
                return map(lambda z: time(*map(int, z.split(':'))), wrap(y, 5))
        else:
            return []
        
    @classmethod
    def get_duration(cls, x):
        y = Parser.get_tdtext(x, 'col_duration')
        if y:
            return time(*map(int, y.split(":")))
        else:
            return None

    def __iter__(self):
        for detail in self.details():
            yield detail

    def _parse_details(self):
        if self._current_state < 0:
            raise ParserError('Unable to parse details while in error state')

        tours = self.soup.findAll('div', {'class': 'data_table tourdetail'})

        trips = map(lambda x: map(lambda y: {
                        'time': Parser.get_time(y),
                        'station': map(lambda z: z[2:].strip(),
                                       filter(lambda x: type(x) == NavigableString, y.find('td', {'class': 'col_station'}).contents)), # filter non NaviStrings
                        'info': map(lambda x: x.strip(),
                                    filter(lambda z: type(z) == NavigableString, y.find('td', {'class': 'col_info'}).contents)),
                    }, x.find('tbody').findAll('tr')),
                    tours) # all routes
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

        # get overview table
        table = self.soup.find('table', {'id': 'tbl_fahrten'})

        # check if there is an overview table
        if table and table.findAll('tr'):
            # get rows
            rows = table.findAll('tr')[1:] # cut off headline
            
            overview = map(lambda x: {
                               'date': Parser.get_date(x),
                               'time': Parser.get_time(x),
                               'duration': Parser.get_duration(x), # grab duration
                               'change': Parser.get_change(x), 
                               'price': Parser.get_price(x),
                           },
                           rows)
        else:
            #self._current_state = self.STATE_ERROR
            raise ParserError('Unable to parse details')

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

    def __init__(self):
        self._stations = {}
        self._lines = []

    def get_stations(self, letter):
        if not self._stations.has_key(letter):
            bs = BeautifulSoup(urllib2.urlopen(settings.stations % letter))
            self._stations[letter] = map(lambda x: x['value'], bs.find('select', {'id': 'letter'}).findAll('option'))

        return self._stations[letter]

    def get_lines(self):
        if not self._lines:
            bs = BeautifulSoup(urllib2.urlopen(settings.line_overview))
            # get tables
            lines = bs.findAll('table', {'class': 'linie'})
            # cut line parameter out of href
            self._lines = map(lambda x: map(lambda x: x['href'][x['href'].find('=') + 1:], x.findAll('a')), lines)

        return self._lines
