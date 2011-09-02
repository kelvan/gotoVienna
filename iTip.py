from BeautifulSoup import BeautifulSoup
import urllib2
import settings

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
            lines = bs.findAll('td', {'class': 'linie'})
            self._lines = []
            
            for line in lines:
                if line.a:
                    print line.text
                    if line.text:
                        self._lines.append((line.text, line.a['href']))
                    elif line.img:
                        self._lines.append((line.img['alt'], line.a['href']))
                        
        return self._lines