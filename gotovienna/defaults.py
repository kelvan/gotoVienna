from os import path

# route search
folder = path.dirname(__file__)
action = 'http://efa.vor.at/wvb/XSLT_TRIP_REQUEST2'
hist_file = path.join(folder, '.wl_history')

# iTip

line_overview = 'http://www.wienerlinien.at/itip/linienwahl/'
stations = 'http://www.wienerlinien.at/itip/haltestelle?letter=%s'

search_post = {'language': 'de',
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
            'place_origin': 'Wien', # overwrite if necessary
            'type_origin': None, # stop/address/poi
            'nameState_origin': 'empty',
            'nameInfo_origin': 'invalid',
            'anyType_origin': '',
            'name_origin': None,
            'typeInfo_destination': 'invalid',
            'placeState_destination': 'empty',
            'placeInfo_destination': 'invalid',
            'place_destination': 'Wien', # overwrite if necessary
            'type_destination': None, # stop/address/poi
            'nameState_destination': 'empty',
            'nameInfo_destination': 'invalid',
            'anyType_destination': '', # maybe nice
            'name_destination': None,
            'itdTripDateTimeDepArr': 'dep',
            'itdDateDayMonthYear': None, # DD.MM.YYYY
            'itdTime': None, # HH:MM
            'submitbutton': 'SUCHEN'
        }