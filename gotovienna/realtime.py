# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import time
import argparse
import re

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
                print 'Invalid time: %s' % time
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

