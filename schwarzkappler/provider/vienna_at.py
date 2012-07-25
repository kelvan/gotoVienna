from abstract import Provider
from datetime import timedelta, datetime

class ViennaAt(Provider):
    provider_name = 'vienna.at'
    update_intervall = timedelta(minutes=30)
    last_updated = None
    url = 'http://apps.vienna.at/tools/schwarzkappler/'
    info = {}

    @classmethod
    def fetch(cls):
        p = cls.get_soup().find('div', {'class':'R1024VIENNA_LeftColumn'}).findAll('p')
        
        cls.info = {}
        for i in range(2):
            if p[i].b:
                for line in p[i].b.text.split(', '):
                    if cls.info.has_key(line):
                        cls.info[line].append({'reportDate': datetime.now().date() + timedelta(i)})
                else:
                    cls.info[line] = [{'reportDate': datetime.now().date()}]
            else:
                print 'ParserError: no bold text found at "%s"' % p[i]
        
        cls.last_updated = datetime.now()
