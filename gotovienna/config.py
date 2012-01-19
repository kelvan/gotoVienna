from os import path
try:
    import json
except ImportError:
    import simplejson as json

class JsonConfig:
    def __init__(self):
        self.configfile = path.expanduser('~/.gotovienna/config.json')
        self.conf = {}
        if path.exists(self.configfile):
            with open(self.configfile, 'r') as f:
                try:
                    self.conf = json.load(f)
                except ValueError:
                    print "Corrupt config"

    def save(self):
        with open(self.configfile, 'w') as f:
            json.dump(self.conf, f)

    def getGpsEnabled(self):
        if self.conf.has_key('gps_enabled'):
            return self.conf['gps_enabled']
        return True

    def setGpsEnabled(self, value):
        self.conf['gps_enabled'] = value
        self.save()

    def getLastStationsUpdate(self):
        if self.conf.has_key('last_stations_update'):
            return self.conf['last_stations_update']
        return 'Unknown'

    def setLastStationsUpdate(self, date):
        self.conf['last_stations_update'] = date
        self.save()

config = JsonConfig()
