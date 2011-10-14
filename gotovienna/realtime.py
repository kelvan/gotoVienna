# -*- coding: utf-8 -*-

from gotovienna.BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import time
import re
import collections
from errors import LineNotFoundError, StationNotFoundError

from gotovienna import defaults

class ITipParser:
    def __init__(self):
        self._stations = {}
        self._lines = {}

    def get_stations(self, name):
        """ Get station by direction
        {'Directionname': [('Station name', 'url')]}
        """
        if not self._stations.has_key(name):
            st = {}

            if not self.lines.has_key(name):
                return None

            bs = BeautifulSoup(urlopen(self.lines[name]))
            tables = bs.findAll('table', {'class': 'text_10pix'})
            for i in range(2):
                dir = tables[i].div.contents[-1].strip('&nbsp;')

                sta = []
                for tr in tables[i].findAll('tr', {'onmouseout': 'obj_unhighlight(this);'}):
                    if tr.a:
                        sta.append((tr.a.text, defaults.line_overview + tr.a['href']))
                    else:
                        sta.append((tr.text.strip('&nbsp;'), None))

                st[dir] = sta
            self._stations[name] = st

        return self._stations[name]

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
        """ Get list of next departures
        integer if time until next departure
        time if time of next departure
        """

        #TODO parse line name and direction for station site parsing

        if not url:
            # FIXME prevent from calling this method with None
            return []

        bs = BeautifulSoup(urlopen(url))
        result_lines = bs.findAll('table')[-1].findAll('tr')

        dep = []
        for tr in result_lines[1:]:
            th = tr.findAll('th')
            if len(th) < 2:
                #TODO replace with logger
                print "[DEBUG] Unable to find th in:\n%s" % str(tr)
                continue

            # parse time
            time = th[-2].text.split(' ')
            if len(time) < 2:
                #print 'Invalid time: %s' % time
                # TODO: Issue a warning OR convert "HH:MM" format to countdown
                continue

            time = time[1]

            if time.find('rze...') >= 0:
                    dep.append(0)
            elif time.isdigit():
                # if time to next departure in cell convert to int
                dep.append(int(time))
            else:
                # check if time of next departue in cell
                t = time.strip('&nbsp;').split(':')
                if len(t) == 2 and all(map(lambda x: x.isdigit(), t)):
                    t = map(int, t)
                    dep.append(time(*t))
                else:
                    # Unexpected content
                    #TODO replace with logger
                    print "[DEBUG] Invalid data:\n%s" % time

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


class Line:
    def __init__(self, name):
        self._stations = None
        self.parser = ITipParser()
        if name.strip() in self.parser.lines():
            self.name = name.strip()
        else:
            raise LineNotFoundError('There is no line "%s"' % name.strip())
        
    @property
    def stations(self):
        if not self._stations:
            self._stations = parser.get_stations(self.name)
        return self._stations
    
    def get_departures(self, stationname):
        stationname = stationname.strip().lower()
        stations = self.stations
        
        found = false
        
        for direction in stations.keys():
            # filter stations starting with stationname
            stations[direction] = filter(lambda station: station[0].lower().starts_with(stationname), stations)
            found = found or bool(stations[direction])
        
        if found:
            # TODO return departures
            raise NotImplementedError()
        else:
            raise StationNotFoundError('There is no stationname called "%s" at route of line "%s"' % (stationname, self.name))