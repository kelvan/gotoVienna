#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from gotovienna.BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from urllib import urlencode
from datetime import datetime, time, timedelta
from textwrap import wrap
import sys
import os.path
import re

from gotovienna import defaults

POSITION_TYPES = ('stop', 'address', 'poi')
TIMEFORMAT = '%H:%M'
DEBUGLOG = os.path.expanduser('~/gotoVienna.debug')

class ParserError(Exception):

    def __init__(self, msg='Parser error'):
        self.message = msg

class PageType:
    UNKNOWN, CORRECTION, RESULT = range(3)


def extract_city(station):
    """ Extract city from string if present,
    else return default city
    
    >>> extract_city('Karlsplatz, Wien')
    'Wien'
    """
    if len(station.split(',')) > 1:
        return station.split(',')[-1].strip()
    else:
        return 'Wien'
        
def extract_station(station):
    """ Remove city from string
    
    >>> extract_station('Karlsplatz, Wien')
    'Karlsplatz'
    """
    if len(station.split(',')) > 1:
        return station[:station.rindex(',')].strip()
    else:
        return station
    
def split_station(station):
    """ >>> split_station('Karlsplatz, Wien')
    ('Karlsplatz', 'Wien')
    >>> split_station('Karlsplatz')
    ('Karlsplatz', 'Wien')
    """
    if len(station.split(',')) > 1:
        return (station[:station.rindex(',')].strip(), station.split(',')[-1].strip())
    else:
        return (station, 'Wien')

def guess_location_type(location):
    """Guess type (stop, address, poi) of a location

    >>> guess_location_type('pilgramgasse')
    'stop'

    >>> guess_location_type('karlsplatz 14')
    'address'

    >>> guess_location_type('reumannplatz 12/34')
    'address'
    """
    parts = location.split()
    first_part = parts[0]
    last_part = parts[-1]

    # Assume all single-word locations are stops
    if len(parts) == 1:
        return 'stop'

    # If the last part is numeric, assume address
    if last_part.isdigit() and len(parts) > 1:
        return 'address'

    # Addresses with door number (e.g. "12/34")
    if all(x.isdigit() or x == '/' for x in last_part):
        return 'address'

    # Sane default - assume it's a stop/station name
    return 'stop'

def search(origin_tuple, destination_tuple, dtime=None):
    """ build route request
    returns html result (as urllib response)
    """
    if not dtime:
        dtime = datetime.now()

    origin, origin_type = origin_tuple
    origin, origin_city = split_station(origin)
    
    destination, destination_type = destination_tuple
    destination, destination_city = split_station(destination)


    if origin_type is None:
        origin_type = guess_location_type(origin)
        print 'Guessed origin type:', origin_type

    if destination_type is None:
        destination_type = guess_location_type(destination)
        print 'Guessed destination type:', destination_type

    if (origin_type not in POSITION_TYPES or
            destination_type not in POSITION_TYPES):
        raise ParserError('Invalid position type')

    post = defaults.search_post
    post['name_origin'] = origin
    post['type_origin'] = origin_type
    post['name_destination'] = destination
    post['type_destination'] = destination_type
    post['itdDateDayMonthYear'] = dtime.strftime('%d.%m.%Y')
    post['itdTime'] = dtime.strftime('%H:%M')
    post['place_origin'] = origin_city
    post['place_destination'] = destination_city
    params = urlencode(post)
    url = '%s?%s' % (defaults.action, params)

    try:
        f = open(DEBUGLOG, 'a')
        f.write(url + '\n')
        f.close()
    except:
        print 'Unable to write to DEBUGLOG: %s' % DEBUGLOG

    return urlopen(url)


class sParser:
    """ Parser for search response
    """

    def __init__(self, html):
        self.soup = BeautifulSoup(html)

    def check_page(self):
        if self.soup.find('form', {'id': 'form_efaresults'}):
            return PageType.RESULT

        if self.soup.find('div', {'class':'form_error'}):
            return PageType.CORRECTION

        return PageType.UNKNOWN

    state = property(check_page)

    def get_correction(self):
        names_origin = self.soup.find('select', {'id': 'nameList_origin'})
        names_destination = self.soup.find('select', {'id': 'nameList_destination'})
        places_origin = self.soup.find('select', {'id': 'placeList_origin'})
        places_destination = self.soup.find('select', {'id': 'placeList_destination'})
        

        if any([names_origin, names_destination, places_origin, places_destination]):
            dict = {}
            
            if names_origin:
                dict['origin'] = map(lambda x: x.text, 
                                     names_origin.findAll('option'))
            if names_destination:
                dict['destination'] = map(lambda x: x.text, 
                                          names_destination.findAll('option'))
                
            if places_origin:
                dict['place_origin'] = map(lambda x: x.text, 
                                           names_origin.findAll('option'))
            if names_destination:
                dict['place_destination'] = map(lambda x: x.text, 
                                                names_destination.findAll('option'))
    
            return dict
        
        else:
            raise ParserError('Unable to parse html')

    def get_result(self):
        return rParser(str(self.soup))



class rParser:
    """ Parser for routing results
    """

    def __init__(self, html):
        self.soup = BeautifulSoup(html)
        self._overview = None
        self._details = None

    @classmethod
    def get_tdtext(cls, x, cl):
            return x.find('td', {'class': cl}).text

    @classmethod
    def get_change(cls, x):
        y = rParser.get_tdtext(x, 'col_change')
        if y:
            return int(y)
        else:
            return 0

    @classmethod
    def get_price(cls, x):
        y = rParser.get_tdtext(x, 'col_price')
        if y == '*':
            return 0.0
        if y.find(','):
            return float(y.replace(',', '.'))
        else:
            return 0.0

    @classmethod
    def get_date(cls, x):
        y = rParser.get_tdtext(x, 'col_date')
        if y:
            return datetime.strptime(y, '%d.%m.%Y').date()
        else:
            return None

    @classmethod
    def get_datetime(cls, x):
        y = rParser.get_tdtext(x, 'col_time')
        if y:
            if (y.find("-") > 0):
                # overview mode
                times = map(lambda z: time(*map(int, z.split(':'))), y.split('-'))
                d = rParser.get_date(x)
                from_dtime = datetime.combine(d, times[0])
                if times[0] > times[1]:
                    # dateline crossing
                    to_dtime = datetime.combine(d + timedelta(1), times[1])
                else:
                    to_dtime = datetime.combine(d, times[1])
                    
                return [from_dtime, to_dtime]
            
            else:
                dtregex = {'date' : '\d\d\.\d\d',
                           'time': '\d\d:\d\d'}
                
                regex = "\s*(?P<date1>{date})?\s*(?P<time1>{time})\s*(?P<date2>{date})?\s*(?P<time2>{time})\s*".format(**dtregex)
                ma = re.match(regex, y)
                
                if not ma:
                    return []
                
                gr = ma.groupdict()
                
                def extract_datetime(gr, n):
                    if 'date%d' % n in gr and gr['date%d' % n]:
                        from_dtime = datetime.strptime(str(datetime.today().year) + gr['date%d' % n] + gr['time%d' % n], '%Y%d.%m.%H:%M')
                    else:
                        t = datetime.strptime(gr['time%d' % n], '%H:%M').time()
                        d = datetime.today().date()
                        return datetime.combine(d, t)
                
                # detail mode
                from_dtime = extract_datetime(gr, 1)
                to_dtime = extract_datetime(gr, 2)
                
                return [from_dtime, to_dtime]
                
        else:
            return []

    def __iter__(self):
        for detail in self.details():
            yield detail

    def _parse_details(self):
        tours = self.soup.findAll('div', {'class': 'data_table tourdetail'})

        trips = map(lambda x: map(lambda y: {
                        'timespan': rParser.get_datetime(y),
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
                               'timespan': rParser.get_datetime(x),
                               'change': rParser.get_change(x),
                               'price': rParser.get_price(x),
                           },
                           rows)
        else:
            raise ParserError('Unable to parse overview')

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
                f = open(DEBUGLOG, 'w')
                f.write(str(self.soup))
                f.close()

        return self._overview

