from BeautifulSoup import BeautifulSoup, NavigableString
from urllib2 import urlopen
from urllib import urlencode
import settings
from datetime import datetime, time
from textwrap import wrap
import argparse
import sys

POSITION_TYPES = ('stop', 'address', 'poi')
TIMEFORMAT = '%H:%M'

class ParserError(Exception):
    
    def __init__(self, msg='Parser error'):
        self.message = msg

class PageType:
    UNKNOWN, CORRECTION, RESULT = range(3)
    

def search(origin_tuple, destination_tuple, dtime=None):
    """ build route request
    returns html result (as urllib response)
    """
    if not dtime:
        dtime = datetime.now()
    
    origin, origin_type = origin_tuple
    destination, destination_type = destination_tuple
    if not origin_type in POSITION_TYPES or\
        not destination_type in POSITION_TYPES:
        raise ParserError('Invalid position type')
        
    post = settings.search_post
    post['name_origin'] = origin
    post['type_origin'] = origin_type
    post['name_destination'] = destination
    post['type_destination'] = destination_type
    post['itdDateDayMonthYear'] = dtime.strftime('%d.%m.%Y')
    post['itdTime'] = dtime.strftime('%H:%M')
    params = urlencode(post)
    url = '%s?%s' % (settings.action, params)
    
    print "\nurl %s url\n\n%s\n\nurl %s url\n" % ('~' * 100, url, '~' * 100)
    
    return urlopen(url)


class sParser:
    """ Parser for search response
    """

    def __init__(self, html):
        self.soup = BeautifulSoup(html)
    
    def check_page(self):
        if self.soup.find('form', {'id': 'form_efaresults'}):
            return PageType.RESULT
        
        if self.soup.find('div', {'class':'form_error'}):
            return PageType.CORRECTION
        
        return PageType.UNKNOWN
    
    def get_correction(self):
        nlo = self.soup.find('select', {'id': 'nameList_origin'})
        nld = self.soup.find('select', {'id': 'nameList_destination'})
        
        if not nlo and not nld:
            raise ParserError('Unable to parse html')
        
        if nlo:
            origin = map(lambda x: x.text, nlo.findAll('option'))
        else:
            origin = []
        if nld:
            destination = map(lambda x: x.text, nld.findAll('option'))
        else:
            destination = []
        
        return (origin, destination)
    
    def get_result(self):
        return rParser(str(self.soup))
        
        
        
class rParser:
    """ Parser for routing results
    """

    def __init__(self, html):
        self.soup = BeautifulSoup(html)
        self._overview = None
        self._details = None

    @classmethod
    def get_tdtext(cls, x, cl):
            return x.find('td', {'class': cl}).text
    
    @classmethod
    def get_change(cls, x):
        y = rParser.get_tdtext(x, 'col_change')
        if y:
            return int(y)
        else:
            return 0

    @classmethod
    def get_price(cls, x):
        y = rParser.get_tdtext(x, 'col_price')
        if y.find(','):
            return float(y.replace(',', '.'))
        else:
            return 0.0

    @classmethod
    def get_date(cls, x):
        y = rParser.get_tdtext(x, 'col_date')
        if y:
            return datetime.strptime(y, '%d.%m.%Y').date()
        else:
            return None
        
    @classmethod
    def get_time(cls, x):
        y = rParser.get_tdtext(x, 'col_time')
        if y:
            if (y.find("-") > 0):
                return map(lambda z: time(*map(int, z.split(':'))), y.split('-'))
            else:
                return map(lambda z: time(*map(int, z.split(':'))), wrap(y, 5))
        else:
            return []
        
    @classmethod
    def get_duration(cls, x):
        y = rParser.get_tdtext(x, 'col_duration')
        if y:
            return time(*map(int, y.split(":")))
        else:
            return None

    def __iter__(self):
        for detail in self.details():
            yield detail

    def _parse_details(self):
        tours = self.soup.findAll('div', {'class': 'data_table tourdetail'})

        trips = map(lambda x: map(lambda y: {
                        'time': rParser.get_time(y),
                        'station': map(lambda z: z[2:].strip(),
                                       filter(lambda x: type(x) == NavigableString, y.find('td', {'class': 'col_station'}).contents)), # filter non NaviStrings
                        'info': map(lambda x: x.strip(),
                                    filter(lambda z: type(z) == NavigableString, y.find('td', {'class': 'col_info'}).contents)),
                    }, x.find('tbody').findAll('tr')),
                    tours) # all routes
        return trips

    @property
    def details(self):
        """returns list of trip details
        [ [ { 'time': [datetime.time, datetime.time] if time else [],
              'station': [u'start', u'end'] if station else [],
              'info': [u'start station' if station else u'details for walking', u'end station' if station else u'walking duration']
            }, ... # next trip step 
          ], ... # next trip possibility
        ]
        """
        if not self._details:
            self._details = self._parse_details()

        return self._details

    def _parse_overview(self):

        # get overview table
        table = self.soup.find('table', {'id': 'tbl_fahrten'})

        # check if there is an overview table
        if table and table.findAll('tr'):
            # get rows
            rows = table.findAll('tr')[1:] # cut off headline
            
            overview = map(lambda x: {
                               'date': rParser.get_date(x),
                               'time': rParser.get_time(x),
                               'duration': rParser.get_duration(x), # grab duration
                               'change': rParser.get_change(x),
                               'price': rParser.get_price(x),
                           },
                           rows)
        else:
            raise ParserError('Unable to parse overview')

        return overview

    @property
    def overview(self):
        """dict containing
        date: datetime
        time: [time, time]
        duration: time
        change: int
        price: float
        """
        if not self._overview:
            try:
                self._overview = self._parse_overview()
            except AttributeError:
                f = open('DEBUG', 'w')
                f.write(str(self.soup))
                f.close()

        return self._overview

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Get public transport route for Vienna')
    parser.add_argument('-o', metavar='name', type=str, help='origin', required=True)
    parser.add_argument('-d', metavar='name', type=str, help='destination', required=True)
    parser.add_argument('-ot', metavar='type', type=str, help='origin type: %s' % ' | '.join(POSITION_TYPES), default='stop', choices=POSITION_TYPES)
    parser.add_argument('-dt', metavar='type', type=str, help='destination type: %s' % ' | '.join(POSITION_TYPES), default='stop', choices=POSITION_TYPES)

    args = parser.parse_args()
    
    html = search((args.o.encode('UTF-8'), args.ot), (args.d.encode('UTF-8'), args.dt)).read()
    
    parser = sParser(html)
    state = parser.check_page()
    
    if state == PageType.CORRECTION:
        try:
            cor = parser.get_correction()
            if cor[0]:
                print
                print '* Origin ambiguous:'
                lo = None
                while not lo or not lo.isdigit() or int(lo) > len(cor[0]):
                    i = 1
                    for c in cor[0]:
                        print '%d. %s' % (i, c)
                        i += 1
                    lo = sys.stdin.readline().strip()
                
                args.o = cor[0][int(lo) - 1]
                
            if cor[1]:
                print
                print '* Destination ambiguous:'
                ld = None
                while not ld or not ld.isdigit() or int(ld) > len(cor[1]):
                    j = 1
                    for c in cor[1]:
                        print '%d. %s' % (j, c)
                        j += 1
                    ld = sys.stdin.readline().strip()
                    
                args.d = cor[1][int(ld) - 1]
            
            html = search((args.o.encode('UTF-8'), args.ot), (args.d.encode('UTF-8'), args.dt)).read()
    
            parser = sParser(html)
            state = parser.check_page()
            
        except ParserError:
            print 'PANIC at correction page'
            
    if state == PageType.RESULT:
        parser = rParser(html)
        try:
            overviews = parser.overview
            details = parser.details
            l = ''
            while not l == 'q':
                for r in range(len(overviews)):
                    print '%d. [%s] %s-%s (%s)' % (r + 1, overviews[r]['date'], overviews[r]['time'][0], overviews[r]['time'][1], overviews[r]['duration'])
                print 'q. Quit'
                l = sys.stdin.readline().strip()
                print
                print '~' * 100
                
                if l.isdigit() and int(l) <= len(details):
                    for detail in details[int(l) - 1]:
                        if detail['time'] and detail['station']:
                            time = '%s - %s' % (detail['time'][0].strftime(TIMEFORMAT), detail['time'][1].strftime(TIMEFORMAT))
                            print '[%s] %s\n%s' % (time, ' -> '.join(detail['station']), '\n'.join(detail['info']))
                        else:
                            print '\n'.join(detail['info'])
                        print '-' * 100
                print
                
        except ParserError:
            print 'parsererror'
            
    elif state == PageType.UNKNOWN:
        print 'PANIC unknown result'
