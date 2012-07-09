from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen
from datetime import datetime

class Provider:
    provider_name = 'generic'
    
    def fetch(self):
        pass

    @classmethod
    def need_update(cls):
        if not cls.last_updated:
            return True
        
        return cls.last_updated + cls.update_intervall < datetime.now()

    @classmethod
    def get_soup(cls):
        return BeautifulSoup(urlopen(cls.url))
