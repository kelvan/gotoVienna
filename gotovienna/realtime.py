# -*- coding: utf-8 -*-

from gotovienna.BeautifulSoup import BeautifulSoup
#from urllib2 import urlopen
from urllib import quote_plus
# Use urlopen proxy for fake user agent
from UrlOpener import urlopen
from datetime import time, datetime, timedelta
import datetime as date
import re
import collections
from errors import LineNotFoundError, StationNotFoundError
import cache
from cache import Stations
from time import sleep
from utils import sort_departures

from gotovienna import defaults

class Departure(dict):
    def __init__(self, line, station, direction, time, lowfloor):
        self['line'] = line
        self['station'] = station
        self['direction'] = direction
        now = datetime.now()
        if type(time) == date.time:
            time = make_datetime(now, time)
        if type(time) == datetime:
            # FIXME convert in ModelList
            self['realtime'] = False
            self['time'] = (time - now).seconds/60
            self['departure'] = time
        elif type(time) == int:
            # FIXME convert in ModelList
            self['realtime'] = True
            self['time'] = time
            self['departure'] = now + timedelta(minutes=self['time'])
        else:
            raise ValueError('Wrong type: time')

        # FIXME convert in ModelList
        self['ftime'] = str(self['time'])
        self['lowfloor'] = lowfloor

class ITipParser:
    def __init__(self):
        self._lines = cache.lines

    def parse_stations(self, html):
        bs = BeautifulSoup(html)
        tables = bs.findAll('table', {'class': 'text_10pix'})
        st = {}

        for i in range(2):
            dir = tables[i].div.contents[-1].strip()[6:-6]

            sta = []
            for tr in tables[i].findAll('tr', {'onmouseout': 'obj_unhighlight(this);'}):
                if tr.a:
                    sta.append((tr.a.text, defaults.line_overview + tr.a['href']))
                else:
                    sta.append((tr.text.strip('&nbsp;'), None))

            st[dir] = sta
        return st

    def get_stations(self, name):
        """ Get station by direction
        {'Directionname': [('Station name', 'url')]}
        """
        if not name in self.lines:
            return {}

        st = Stations(name)

        if not st:
            st = self.parse_stations(urlopen(self.lines[name]).read())

        return st

    def parse_lines(self, html):
        """ Parse lines from html
        """
        bs = BeautifulSoup(html)
        # get tables
        lines = bs.findAll('td', {'class': 'linie'})

        l = {}

        for line in lines:
            if line.a:
                href = defaults.line_overview + line.a['href']
                if line.text:
                    l[line.text] = href
                elif line.img:
                    l[line.img['alt']] = href

        return l

    @property
    def lines(self):
        """ Dictionary of Line names with url as value
        """
        if not self._lines:
            self._lines = self.parse_lines(urlopen(defaults.line_overview).read())

        return self._lines

    def get_url_from_direction(self, line, direction, station):
        stations = self.get_stations(line)

        for stationname, url in stations.get(direction, []):
            if stationname == station:
                return url

        return None

    def parse_departures_by_station(self, html):
        """ Parse departure page
        precondition: html is correct departure page
        handle select station page before calling this method
        """
        bs = BeautifulSoup(html)
        dep = []

        try:
            li = bs.ul.findAll('li')

            station = bs.strong.text.split(',')[0]

            for l in li:
                try:
                    d = l.div.next
                    if d.find('&raquo;') == -1:
                        d = d.next.next

                    direction = d.replace('&raquo;', '').strip()
                    if direction.startswith('NICHT EINSTEIGEN'):
                        continue

                    line = l.img['alt']
                    for span in l.findAll('span'):
                        if span.text.isdigit():
                            tim = int(span.text)
                        elif span.text.find(':') >= 0:
                            tim = time(*map(int, span.text.split(':')))
                        else:
                            print 'Warning: %s' % span.text
                            continue

                        if span['class'] == 'departureBarrierFree':
                            lowfloor = True
                        else:
                            lowfloor = False

                        dep.append(Departure(line, station, direction, tim, lowfloor))

                except Exception as e:
                    print 'Warning: %s' % e.message
                    continue

        except AttributeError:
            print 'Error while getting station %s' % station

        finally:
            return dep

    def get_departures_by_station(self, station):
        """ Get list of Departures for one station
        """

        # TODO 1. Error handling
        # TODO 2. more error handling
        # TODO 3. ultimative error handling

        html = urlopen(defaults.departures_by_station % quote_plus(station.encode('UTF-8'))).read()

        li = BeautifulSoup(html).ul.findAll('li')

        if li[0].a:
            # Dirty workaround for ambiguous station
            html = urlopen(defaults.qando + li[0].a['href']).read()

        dep = self.parse_departures_by_station(html)

        self.parse_departures_by_station(html)
        return dep

    def parse_departures(self, html):
        bs = BeautifulSoup(html)

        # Check for error messages
        msg = bs.findAll('span', {'class': 'rot fett'})
        if msg and len(msg) > 0 and unicode(msg[0].text).find(u'technischen St') > 0:
            print '\n'.join(map(lambda x: x.text.replace('&nbsp;', ''), msg))
            return []
        
        mainform = bs.find('form', {'name': 'mainform'})
        if not mainform:
            return []
        
        lines = mainform.table.findAll('tr')[1]

        if len(lines.findAll('td', {'class': 'info'})) > 0:
            station = lines.span.text.replace('&nbsp;', '')
            line = lines.findAll('span')[-1].text.replace('&nbsp;', '')
        else:
            station = lines.td.span.text.replace('&nbsp;', '')
            line = lines.find('td', {'align': 'right'}).span.text.replace('&nbsp;', '')

        result_lines = bs.findAll('table')[-1].findAll('tr')

        dep = []
        for tr in result_lines[1:]:
            d = {'station': station}
            th = tr.findAll('th')

            if len(th) < 2:
                #TODO replace with logger
                print "[DEBUG] Unable to find th in:\n%s" % str(tr)
            elif len(th) == 2:
                # underground site looks different -.-
                d['lowfloor'] = True
                d['line'] = line
                d['direction'] = th[0].text.replace('&nbsp;', '')
                t = th[-1]
            else:
                # all other lines
                d['lowfloor'] = th[-1].find('img') and th[-1].img.has_key('alt')
                d['line'] = th[0].text.replace('&nbsp;', '')
                d['direction'] = th[1].text.replace('&nbsp;', '')
                t = th[-2]
            # parse time
            tim = t.text.split(' ')
            if len(tim) < 2:
                # print '[WARNING] Invalid time: %s' % time
                # TODO: Issue a warning OR convert "HH:MM" format to countdown
                tim = tim[0]
            else:
                tim = tim[1]

            if tim.find('rze...') >= 0:
                    d['time'] = 0
            elif tim.isdigit():
                # if time to next departure in cell convert to int
                d['time'] = int(tim)
            else:
                # check if time of next departue in cell
                t = tim.strip('&nbsp;').split(':')
                if len(t) == 2 and all(map(lambda x: x.isdigit(), t)):
                    t = map(int, t)
                    d['time'] = make_datetime(datetime.now(), time(*t))
                else:
                    # Unexpected content
                    #TODO replace with logger
                    print "[DEBUG] Invalid data:\n%s" % time

            dep.append(Departure(**d))

        return dep

    def get_departures(self, url):
        """ Get list of next departures as Departure objects
        """

        #TODO parse line name and direction for station site parsing

        if not url:
            # FIXME prevent from calling this method with None
            print "ERROR empty url"
            return []

        # open url for 90 min timeslot / get departure for next 90 min
        retry = 0
        tries = 2 # try a second time before return empty list

        while retry < tries:
            html = urlopen(url + "&departureSizeTimeSlot=90").read()
            dep = self.parse_departures(html)

            if dep:
                return dep

            retry += 1
            if retry == tries:
                return []

            sleep(0.5)

    def get_departures_test(self, line, station):
        """ replacement for get_departure
            hide url in higher levels :)
        """
        raise NotImplementedError


UBAHN, TRAM, BUS, NIGHTLINE, OTHER = range(5)
LINE_TYPE_NAMES = ['U-Bahn', 'Strassenbahn', 'Bus', 'Nightline', 'Andere']

def get_line_sort_key(name):
    """Return a sort key for a line name

    >>> get_line_sort_key('U6')
    ('U', 6)

    >>> get_line_sort_key('D')
    ('D', 0)

    >>> get_line_sort_key('59A')
    ('A', 59)
    """
    txt = ''.join(x for x in name if not x.isdigit())
    num = ''.join(x for x in name if x.isdigit()) or '0'

    return (txt, int(num))

def get_line_type(name):
    """Get the type of line for the given name

    >>> get_line_type('U1')
    UBAHN
    >>> get_line_type('59A')
    BUS
    """
    if name.isdigit():
        return TRAM
    elif name.endswith('A') or name.endswith('B') and name[1].isdigit():
        return BUS
    elif name.startswith('U'):
        return UBAHN
    elif name.startswith('N'):
        return NIGHTLINE
    elif name in ('D', 'O', 'VRT', 'WLB'):
        return TRAM

    return OTHER

def categorize_lines(lines):
    """Return a categorized version of a list of line names

    >>> categorize_lines(['U4', 'U3', '59A'])
    [('U-Bahn', ['U3', 'U4']), ('Bus', ['59A'])]
    """
    categorized_lines = collections.defaultdict(list)

    for line in sorted(lines):
        line_type = get_line_type(line)
        categorized_lines[line_type].append(line)

    for lines in categorized_lines.values():
        lines.sort(key=get_line_sort_key)

    return [(LINE_TYPE_NAMES[key], categorized_lines[key])
        for key in sorted(categorized_lines)]

def make_datetime(date, time):
    """ Ugly workaround, immutable datetime ftw -.-
        If 
    """
    if date.hour > time.hour:
        date = date + timedelta(1)
    return datetime(year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=time.hour,
                    minute=time.minute,
                    second=time.second)
