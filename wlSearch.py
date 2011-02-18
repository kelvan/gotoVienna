import urllib
import sys
from datetime import datetime
import settings
import webbrowser
import urllib2


class Search:

    def __init__(self, origin, destination, origin_type='stop', destination_type='stop'):
        self.origin = origin
        self.destination = destination
        self.origin_type = origin_type
        self.destination_type = destination_type

    def get_html(self, dtime=datetime.now()):
        return urllib2.urlopen('%s?%s' % (settings.action, self.get_parameter(dtime)))

    def open_browser(self, dtime=datetime.now()):
        webbrowser.open('%s?%s' % (settings.action, self.get_parameter(dtime)))

    def get_datetime(self, dtime):
        return (dtime.strftime('%d.%m.%Y'), dtime.strftime('%H:%M'))

    def get_parameter(self, dtime):
        date, time = self.get_datetime(dtime)

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
            'itdDateDayMonthYear': date, # DD.MM.YYYY
            'itdTime': time, # HH:MM
            'submitbutton': 'SUCHEN'
        }

        params = urllib.urlencode(post)
        return params
