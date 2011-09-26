from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
import settings
from datetime import time
import argparse
import re

class iParser:

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
                        sta.append((tr.a.text, settings.line_overview + tr.a['href']))
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
            bs = BeautifulSoup(urlopen(settings.line_overview))
            # get tables
            lines = bs.findAll('td', {'class': 'linie'})
            
            for line in lines:
                if line.a:
                    href = settings.line_overview + line.a['href']
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
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get realtime public transport information for Vienna')
    parser.add_argument('-l', metavar='name', type=str, help='line name')
    parser.add_argument('-s', metavar='name', type=str, help='station name')   

    args = parser.parse_args()
    
    itip = iParser()
    lines = itip.lines
    if args.l:
        l = args.l.upper()
    else:
        l = None
    s = args.s.decode('UTF-8')
    
    if l and l in lines:
        stations = itip.get_stations(l)
        for key in stations.keys():
            if not s:
                print '* %s:' % key
            for station in stations[key]:
                if s:
                    if s.startswith(station[0]) or station[0].startswith(s):
                        # FIXME
                        print '* %s\n  %s .....' % (key, station[0]), itip.get_departures(station[1])
                else:
                    print '    %s' % station[0]
    
    elif not l:
        line = {'U-Bahn': '|', 'Strassenbahn': '|', 'Bus': '|', 'Andere': '|', 'Nightline': '|'}
        lines_sorted = lines.keys()
        lines_sorted.sort()
        for li in lines_sorted:
            if li.isdigit():
                type = 'Strassenbahn'
            elif li.endswith('A') or li.endswith('B') and li[1].isdigit():
                type = 'Bus'
            elif li.startswith('U'):
                type = 'U-Bahn'
            elif li.startswith('N'):
                type = 'Nightline'
            else:
                type = 'Andere'
                
            line[type] += ' %s |' % li
        for kv in line.items():
            print "%s:\n%s" % kv
