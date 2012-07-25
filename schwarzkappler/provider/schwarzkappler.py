from abstract import Provider
from datetime import timedelta, datetime
import re

TIMEDELTA_REGEX = re.compile('vor ((?P<hours>\d+)h )?(?P<minutes>\d+)min')

class Schwarzkappler(Provider):
    provider_name = 'schwarzkappler.info'
    update_intervall = timedelta(minutes=1)
    last_updated = None
    url = 'http://schwarzkappler.info/'
    info = {}

    @classmethod
    def fetch(cls):
        divs = cls.get_soup().findAll('div', {'class': re.compile(r"row_\w*")})
        
        cls.info = {}
        for div in divs:
            line = div.h1.text.strip()
            if line == '!':
                # No reports
                break
            mz = div.find('div', {'class':'meldung_zeit'}).b.text
            r = TIMEDELTA_REGEX.search(mz)
            if r:
                hours = r.group('hours')
                minutes = r.group('minutes')
            else:
                print "time not found in:", mz
                continue
            
            if hours and minutes:
                dt = timedelta(hours=int(hours), minutes=int(minutes))
            elif hours:
                dt = timedelta(hours=int(hours))
            elif minutes:
                dt = timedelta(minutes=int(minutes))
            else:
                print "Error: %s" % mz
                continue
        
            d = datetime.now() - dt
            station = div.find('div', {'class':'meldung_text'}).h1.text
            dest = div.find('div', {'class':'meldung_text'}).span.text.strip()[9:]
            if dest == 'Beide':
                dest = None
            type = div.find('div', {'class':'meldung_zeit'}).span.text
            # TODO fetch extra info from link
                
            if cls.info.has_key(line):
                cls.info[line].append({'reportDate':d, 'type': type, 'destination': dest, 'station': station})
            else:
                cls.info[line] = [{'reportDate':d, 'type': type, 'destination': dest, 'station': station}]
        
        cls.last_updated = datetime.now()
