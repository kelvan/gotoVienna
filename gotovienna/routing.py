#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from urllib import urlencode
import settings
from datetime import datetime, time
from textwrap import wrap
import argparse
import sys
import os.path

POSITION_TYPES = ('stop', 'address', 'poi')
TIMEFORMAT = '%H:%M'
DEBUGLOG = os.path.expanduser('~/gotoVienna.debug')

class ParserError(Exception):

    def __init__(self, msg='Parser error'):
        self.message = msg

class PageType:
    UNKNOWN, CORRECTION, RESULT = range(3)


def search(origin_tuple, destination_tuple, dtime=None):
    """ build route request
    returns html result (as urllib response)
    """
    if not dtime:
        dtime = datetime.now()

    origin, origin_type = origin_tuple
    destination, destination_type = destination_tuple
    if not origin_type in POSITION_TYPES or\
        not destination_type in POSITION_TYPES:
        raise ParserError('Invalid position type')

    post = settings.search_post
    post['name_origin'] = origin
    post['type_origin'] = origin_type
    post['name_destination'] = destination
    post['type_destination'] = destination_type
    post['itdDateDayMonthYear'] = dtime.strftime('%d.%m.%Y')
    post['itdTime'] = dtime.strftime('%H:%M')
    params = urlencode(post)
    url = '%s?%s' % (settings.action, params)

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

    def get_correction(self):
        nlo = self.soup.find('select', {'id': 'nameList_origin'})
        nld = self.soup.find('select', {'id': 'nameList_destination'})

        if not nlo and not nld:
            raise ParserError('Unable to parse html')

        if nlo:
            origin = map(lambda x: x.text, nlo.findAll('option'))
        else:
            origin = []
        if nld:
            destination = map(lambda x: x.text, nld.findAll('option'))
        else:
            destination = []

        return (origin, destination)

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
    def get_time(cls, x):
        y = rParser.get_tdtext(x, 'col_time')
        if y:
            if (y.find("-") > 0):
                return map(lambda z: time(*map(int, z.split(':'))), y.split('-'))
            else:
                return map(lambda z: time(*map(int, z.split(':'))), wrap(y, 5))
        else:
            return []

    @classmethod
    def get_duration(cls, x):
        y = rParser.get_tdtext(x, 'col_duration')
        if y:
            return time(*map(int, y.split(":")))
        else:
            return None

    def __iter__(self):
        for detail in self.details():
            yield detail

    def _parse_details(self):
        tours = self.soup.findAll('div', {'class': 'data_table tourdetail'})

        trips = map(lambda x: map(lambda y: {
                        'time': rParser.get_time(y),
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
                               'date': rParser.get_date(x),
                               'time': rParser.get_time(x),
                               'duration': rParser.get_duration(x), # grab duration
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

