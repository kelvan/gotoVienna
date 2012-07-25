from __future__ import with_statement
from os import path
try:
    import json
except ImportError:
    import simplejson as json
import shutil
import defaults
import realtime

def load(p, typ):
    if path.exists(p):
        try:
            with open(p, 'r') as f:
                j = json.load(f)
                if type(j) == typ:
                    return j
                else:
                    print 'Unexpected content in cache file'
                    print 'rebuilding cache'
                    shutil.move(p, p + '.bak')
        except ValueError:
            # FIXME check if empty
            print 'Corrupt cache file'
            print 'rebuilding cache'
            shutil.move(p, p + '.bak')

    return None

class Lines(dict):
    def __init__(self):
        self.load()

    def __setitem__(self, *args, **kwargs):
        s = dict.__setitem__(self, *args, **kwargs)
        self.save()
        return s

    def save(self):
        with open(defaults.cache_lines, 'w') as fp:
            json.dump(self, fp)

    def load(self):
        l = load(defaults.cache_lines, dict)
        if l:
            self.update(l)

lines = Lines()

class Stations(dict):
    stations = None

    def __init__(self, line):
        """ loads cache files
        behaves as dict of directions/stations of line
        automatically saves cache on updates
        """
        if Stations.stations == None:
            Stations.load()

        self.current_line = line
        if line in Stations.stations:
            self.update(Stations.stations[line])
        # FIXME maybe cause problems in the future, race conditions
        Stations.stations[line] = self

    def __setitem__(self, *args, **kwargs):
        u = dict.__setitem__(self, *args, **kwargs)
        Stations.save()
        return u

    @classmethod
    def save(cls):
        with open(defaults.cache_stations, 'w') as fp:
            json.dump(Stations.stations, fp)

    @classmethod
    def load(cls):
        s = load(defaults.cache_stations, dict)
        if s:
            print "load stations from cache"
            cls.stations = s
        else:
            print "load stations from internet"
            cls.stations = {}
