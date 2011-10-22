from realtime import ITipParser

class Line:
    def __init__(self, name):
        self._stations = None
        self.parser = ITipParser()
        if name.strip() in self.parser.lines():
            self.name = name.strip()
        else:
            raise LineNotFoundError('There is no line "%s"' % name.strip())

    @property
    def stations(self):
        if not self._stations:
            self._stations = parser.get_stations(self.name)
        return self._stations

    def get_departures(self, stationname):
        stationname = stationname.strip().lower()
        stations = self.stations

        found = false

        for direction in stations.keys():
            # filter stations starting with stationname
            stations[direction] = filter(lambda station: station[0].lower().starts_with(stationname), stations)
            found = found or bool(stations[direction])

        if found:
            # TODO return departures
            raise NotImplementedError()
        else:
            raise StationNotFoundError('There is no stationname called "%s" at route of line "%s"' % (stationname, self.name))

class Station:
    def __init__(self):
        pass
