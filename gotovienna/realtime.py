# -*- coding: utf-8 -*-

from gotovienna.BeautifulSoup import BeautifulSoup
#from urllib2 import urlopen
from UrlOpener import urlopen
from datetime import time
import re
import collections
from errors import LineNotFoundError, StationNotFoundError
import cache
from cache import Stations

from gotovienna import defaults

class Departure:
    def __init__(self, line, station, direction, time, lowfloor):
        self.line = line
        self.station = station
        self.direction = direction
        self.time = time
        self.lowfloor = lowfloor

    def get_departure_time(self):
        """ return time object of departure time
        """
        if type(self.time) == time:
            return self.time
        else:
            pass
    def get_departure_deltatime(self):
        """ return int representing minutes until departure
        """
        if type(self.time) == int:
            return self.time
        else:
            pass

    def get_ftime(self):
        if type(self.time) == int:
            return str(self.time)
        elif type(self.time) == time:
            return self.time.strftime('%H:%M')

class ITipParser:
    def __init__(self):
        self._lines = cache.lines

    def get_stations(self, name):
        """ Get station by direction
        {'Directionname': [('Station name', 'url')]}
        """
        if not name in self.lines:
            return {}

        st = Stations(name)

        if not st:
            bs = BeautifulSoup(urlopen(self.lines[name]))
            tables = bs.findAll('table', {'class': 'text_10pix'})
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

    @property
    def lines(self):
        """ Dictionary of Line names with url as value
        """
        if not self._lines:
            bs = BeautifulSoup(urlopen(defaults.line_overview))
            # get tables
            lines = bs.findAll('td', {'class': 'linie'})

            for line in lines:
                if line.a:
                    href = defaults.line_overview + line.a['href']
                    if line.text:
                        self._lines[line.text] = href
                    elif line.img:
                        self._lines[line.img['alt']] = href

        return self._lines

    def get_url_from_direction(self, line, direction, station):
        stations = self.get_stations(line)

        for stationname, url in stations.get(direction, []):
            if stationname == station:
                return url

        return None

    def get_departures(self, url):
        """ Get list of next departures as Departure object
        """

        #TODO parse line name and direction for station site parsing

        if not url:
            # FIXME prevent from calling this method with None
            print "ERROR empty url"
            return []

        # open url for 90 min timeslot / get departure for next 90 min
        retry = 0
        tries = 2
        while retry < tries:
            bs = BeautifulSoup(urlopen(url + "&departureSizeTimeSlot=90"))
            try:
                lines = bs.find('form', {'name': 'mainform'}).table.findAll('tr')[1]
            except AttributeError:
                print 'FetchError'
                msg = bs.findAll('span', {'class': 'rot fett'})
                if len(msg) > 0 and str(msg[0].text).find(u'technischen St') > 0:
                    print 'Temporary problem'
                    print '\n'.join(map(lambda x: x.text.replace('&nbsp;', ''), msg))
                    # FIXME Change to error message after fixing qml gui
                    return []
                # FIXME more testing
                retry += 1
                if retry == tries:
                    return []
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
                d['lowfloor'] = th[-1].has_key('img') and th[-1].img.has_key('alt')
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
                    d['time'] = time(*t)
                else:
                    # Unexpected content
                    #TODO replace with logger
                    print "[DEBUG] Invalid data:\n%s" % time

            print d
            dep.append(Departure(**d))

        return dep


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
