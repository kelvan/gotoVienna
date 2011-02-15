import urllib
import sys
from datetime import datetime
import settings
import webbrowser


class Search:

    def __init__(self, origin, destination, origin_type='stop', destination_type='stop', dtime=datetime.now()):
        self.origin = origin
        self.destination = destination
        self.datetime = dtime
        self.origin_type = origin_type
        self.destination_type = destination_type

    def open_browser(self):
        webbrowser.open('%s?%s' % (settings.action, self.parameter))

    @property
    def time(self):
        return self.datetime.strftime('%H:%M')

    @property
    def date(self):
        return self.datetime.strftime('%d.%m.%Y')

    @property
    def parameter(self):
        post = {'language': 'de',
            'sessionID': 0,
            'requestID': 0,
            'execInst': 'normal',
            'command': '',
            'anySigWhenPerfectNoOtherMatches': 1,
            'itdLPxx_locationServerActive': '',
            'locationServerActive': 0,
            'typeInfo_origin': 'invalid',
            'placeState_origin': 'empty',
            'placeInfo_origin': 'invalid',
            'place_origin': 'Wien',
            'type_origin': self.origin_type, # stop/address/poi
            'nameState_origin': 'empty',
            'nameInfo_origin': 'invalid',
            'anyType_origin': '',
            'name_origin': self.origin,
            'typeInfo_destination': 'invalid',
            'placeState_destination': 'empty',
            'placeInfo_destination': 'invalid',
            'place_destination': 'Wien',
            'type_destination': self.destination_type, # stop/address/poi
            'nameState_destination': 'empty',
            'nameInfo_destination': 'invalid',
            'anyType_destination': '',
            'name_destination': self.destination,
            'itdTripDateTimeDepArr': 'dep',
            'itdDateDayMonthYear': self.date, # DD.MM.YYYY
            'itdTime': self.time, # HH:MM
            'submitbutton': 'SUCHEN'
        }

        params = urllib.urlencode(post)
        return params
