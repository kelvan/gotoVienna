from os import path
import json
import shutil
import defaults
import realtime


def load(path):
    if path.exists(path, typ):
        try:
            with open(path, 'r') as f:
                j = json.load(f)
                if type(j) == typ:
                    return j
                else:
                    print 'Unexpected content in cache file'
                    print 'rebuilding cache'
                    shutil.copy(path, path + '.bak')
        except ValueError:
            print 'Corrupt cache file'
            print 'rebuilding cache'
            shutil.copy(path, path + '.bak')

    return None

class Lines(list):
    def __init__(self, lines=[]):
        l = load(defaults.cache_line)
        if l and type(l) == list:
            lines = l
        self.lines = lines

    def __iter__(self):
        for line in self.lines:
            yield line
        raise StopIteration()

    def __iadd__(self, y):
        self.lines += y

    def __add__(self, y):
        return self.lines + y

    def __getitem__(self, y):
        return self.lines[y]

    def __len__(self):
        return len(self.lines)

    def __str__(self):
        return str(self.lines)

    def __setitem__(self, i, y):
        self.lines[i] = y

class Stations(dict):
    stations = {}

    def __init__(self, line=False):
        """ loads cache files
        if line=False behaves as dict of all lines/stations
        if line behaves as dict of directions/stations of line
        """
        if not Stations.stations:
            s = load(defaults.cache_line, dict)
            if s:
                Stations.stations = st

        self.current_line = line
        if line == False:
            self.dict = Stations.stations
        elif line in Stations.stations:
            self.dict = Stations.stations[line]
        else:
            Stations.stations[line] = {}
            self.dict = Stations.stations[line]


    def __getitem__(self, *args, **kwargs):
        return self.dict.__getitem__(self, *args, **kwargs)
