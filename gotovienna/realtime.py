# -*- coding: utf-8 -*-

from gotovienna.BeautifulSoup import BeautifulSoup
from urllib2 import HTTPError
from urllib import quote_plus
# Use urlopen proxy for fake user agent
from UrlOpener import urlopen, loadCookie
from datetime import time, datetime, timedelta
import datetime as date
import re
import collections
from errors import LineNotFoundError, StationNotFoundError
import cache
from cache import Stations
from time import sleep
from utils import sort_departures, clean_text
try:
    from Levenshtein import distance
except:
    print "Cannot import Levenshtein.distance, use fallback"
    distance = lambda x, y: (y*1.0) / x

from gotovienna import defaults

DELTATIME_REGEX = re.compile('.*?(\d+).*?')
ABSTIME_REGEX = re.compile('.*(\d{2}:\d{2}).*')
# Linie U2 - Gleis 2: ASPERNSTRASSE N\xc4CHSTER ZUG   6 MIN
ZUSATZTEXT_REGEX = re.compile('Linie ([\w\d]+) - Gleis \d: (\w+) N\xc4CHSTER ZUG   (\d+) MIN')

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
            if time >= now:
                self['time'] = (time - now).seconds/60
            else:
                self['time'] = -1 * (now - time).seconds/60
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
        tables = bs.findAll('table', {'class':'show_fw'})
        st = {}

        for i in range(2):
            trs = tables[i].findAll('tr')
            direction = clean_text(trs[0].text.replace('Fahrtrichtung', ''))
            
            sta = []
            for tr in trs[2:-1]:
                if tr.a:
                    sta.append((clean_text(tr.a.text), defaults.base_url + tr.a['href']))
                else:
                    sta.append((clean_text(tr.text), None))

            st[direction] = sta
        return st

    def get_stations(self, name):
        """ Get station by direction
        {'Directionname': [('Station name', 'url')]}
        """
        if not name in self.lines:
            return {}

        st = Stations(name)

        if not st:
            urlopen(defaults.stations % name)
            st = self.parse_stations(urlopen(defaults.stations % name).read())

        return st

    def parse_lines(self, html):
        """ Parse lines from html
        """
        bs = BeautifulSoup(html)
        # get tables
        lines = bs.findAll('td', {'class':'auswahl'})

        l = {}

        for line in lines:
            if line.a:
                hr = line.a['href'].split('?', 1)[-1]
                href = defaults.station_base + hr
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
            print "Load lines"
            self._lines = self.parse_lines(urlopen(defaults.line_overview).read())
            if not self._lines:
                print "Error fetching lines"

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

        station = station.encode('UTF-8')
        html = urlopen(defaults.departures_by_station % quote_plus(station)).read()

        li = BeautifulSoup(html).ul.findAll('li')

        if li[0].a:
            # calculate levenshtein distance of results
            st = map(lambda x: (distance(station, x.a.text.encode('UTF-8')), x.a.text.encode('UTF-8'), x.a['href']), li)
            # take result with lowest levenshtein distance
            s = min(st)
            lnk = s[2]
            
            if len(st) > 1:
                print "Multiple results found, using best match:", s[1]
            
            html = urlopen(defaults.qando + lnk).read()

        dep = self.parse_departures_by_station(html)

        return dep

    def parse_departures(self, html):
        bs = BeautifulSoup(html)
        dep = []

        # Check for error messages
        msg = bs.findAll('span', {'class': 'rot fett'})
        if msg and len(msg) > 0 and unicode(msg[0].text).find(u'technischen St') > 0:
            print '\n'.join(map(lambda x: x.text.replace('&nbsp;', ''), msg))
            return []
        
        errtable = bs.find('table', {'class':'errortable'})
        if errtable and clean_text(errtable.text):
            print "Errortable found"
            print errtable.text
            return []

        if bs.table and bs.table.tr:
            st_td = bs.table.tr.findAll('td')
        
            if st_td:
                station = clean_text(st_td[-1].text)
            else:
                print "Unexpected Error: Stationname not found"
                print "Debug:", st_td.encode('UTF-8')
        else:
            print "Unexpected Error: table or tr not found"
            print bs
            return []
        
        # zusatztext crap
        zt = bs.find('td', {'class':'zusatztext'})
        if zt:
            ma = ZUSATZTEXT_REGEX.search(zt.text)
            if ma:
                line = ma.group(1)
                direction = ma.group(2)
                if direction == direction.upper():
                    direction = direction.capitalize()
                tim = int(ma.group(3))
                d = Departure(line=line, direction=direction,
                              lowfloor=True, station=station, time=tim)
                dep.append(d)
            else:
                print zt.text
        
        table = bs.find('table', {'class':'imagetable'})
        if not table:
            print "table not found"
            return []
        
        if errtable:
            print "Warning: Empty errortable found"
            return dep
        
        trs = table.findAll('tr')
        
        for tr in trs[1:]:
            tds = tr.findAll('td')
            line = clean_text(tds[0].text)
            direction = clean_text(tds[1].text)
            
            if direction.startswith(line):
                direction = direction.lstrip(line).strip()
                
            if direction == direction.upper():
                direction = direction.capitalize()
            
            lf_img = tds[-1].img
            
            lowfloor = lf_img and lf_img.has_key('alt')
            
            d = {'line': line,
                 'direction': direction,
                 'lowfloor': lowfloor,
                 'station': station}

            # parse time
            tim = clean_text(tds[2].text)
            dts = DELTATIME_REGEX.search(tim)
            abs = ABSTIME_REGEX.search(tim)
            
            if tim.find(u'...in K\xfcrze') >= 0:
                d['time'] = 0
            elif abs:
                d['time'] = calc_datetime(abs.group(1))
            elif tim.isdigit():
                d['time'] = int(tim)
            elif dts:
                # is timedelta
                d['time'] = int(dts.group(1))
            else:
                print "Error parsing time:", tim
                continue

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
            # http://www.wienerlinien.at/itip/linienwahl/anzeige.php?PHPSESSID=8ojk9788jlp69mbqtnqvqaqkg5&departureSizeTimeSlot=70&sortType=abfSort
            try:
                urlopen(url)
                html = urlopen(url + "&departureSizeTimeSlot=70").read()
            except HTTPError:
                print "HTTPError at %s" % url
                return []
                
            dep = self.parse_departures(html)

            if dep:
                return dep

            retry += 1
            if retry == tries:
                return []

            sleep(0.5)


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
    if datetime.now().hour > time.hour:
        date = date + timedelta(1)
    return datetime(year=date.year,
                    month=date.month,
                    day=date.day,
                    hour=time.hour,
                    minute=time.minute,
                    second=time.second)

def calc_datetime(timestr):
    """ Build datetime from time string ('HH:MM')
    """
    hour, minute = timestr.split(':')
    t = time(int(hour), int(minute))
    now = datetime.now() 
    
    day = now.today().date()
    if now.time() > t:
        # time propably tomorrow
        day += 1
        
    return make_datetime(day, t)
