# -*- coding: utf-8 -*-

import urllib
import sys
from datetime import datetime
import settings
import webbrowser
import urllib2

from parseHtml import Parser

from PySide.QtCore import Qt
from PySide.QtDeclarative import QDeclarativeView

def QMLModel(overview, details):
    # Mapping from the "overview" data structure to a "plain" data
    # structure to be used as model for the qml listview
    r = []
    i = 0
    for item in overview:
        d = {
                'date': item['date'].strftime('%d.%m.%Y') if item['date'] else u'Fußweg',
                'duration': item['duration'].strftime('%H:%M'),
                'price': item['price'],
                'change': item['change'],
                'details': details[i],
        }

        if len(item['time']) == 2 and all(x is not None for x in item['time']):
            d.update({
                'time_from': item['time'][0].strftime('%H:%M'),
                'time_to': item['time'][1].strftime('%H:%M'),
            })
        else:
            d.update({'time_from': '-', 'time_to': '-'})

        r.append(d)
        i += 1
    return r


class Search:

    def __init__(self, origin, destination, origin_type='stop', destination_type='stop', parent=None):
        self.origin = origin
        self.destination = destination
        self.origin_type = origin_type
        self.destination_type = destination_type
        self.parent = parent
        self.view = None
        self.qml_model = None

    def get_html(self, dtime=None):
        if not dtime:
            dtime = datetime.now()
        #FIXME replace with logger
        print "get_html (%s:%s:%s)" % tuple(dtime.timetuple())[3:6]
        return urllib2.urlopen('%s?%s' % (settings.action, self.get_parameter(dtime)))

    def open_browser(self, dtime=datetime.now()):
        webbrowser.open('%s?%s' % (settings.action, self.get_parameter(dtime)))

    def open_qml(self, dtime=None):
        if not dtime:
            dtime = datetime.now()
        #FIXME replace with logger
        print "open_qml (%s:%s:%s)" % tuple(dtime.timetuple())[3:6]
        p = Parser(self.get_html(dtime))
        self.qml_model = QMLModel(p.overview, p.details)
        self.view = QDeclarativeView(self.parent)
        self.view.setWindowTitle('Search results')
        self.view.setWindowFlags(Qt.Window)
        # quick & dirty workaround
        try:
            self.view.setAttribute(Qt.WA_Maemo5StackedWindow)
        except:
            pass
        self.view.setResizeMode(QDeclarativeView.SizeRootObjectToView)
        self.view.setSource('ui/Overview.qml')
        self.view.rootObject().setProperty('model', self.qml_model)
        self.view.show()

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
