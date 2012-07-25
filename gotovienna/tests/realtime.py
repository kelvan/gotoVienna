# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_true, assert_false, assert_is_instance
import sys
import os
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
DATAPATH = os.path.join(os.path.dirname(__file__), 'data')

# bananas for the monkey
class datetime_static(datetime):
    @classmethod
    def now(cls):
        return datetime(2000, 1, 1, 11, 50) 

from gotovienna import realtime
realtime.datetime = datetime_static
from gotovienna.realtime import *
# </bananas>

parser = ITipParser()

def load_data(filename):
    return open(os.path.join(DATAPATH, filename), 'r').read()

stationbased = load_data('stationbased.html')
lines = load_data('lines.html')

def test_lines():
    parsed_lines = parser.parse_lines(lines)
    assert_is_instance(parsed_lines, dict)
    assert_true(parsed_lines)

def test_line_amount():
    parsed_lines = parser.parse_lines(lines)
    assert_equal(102, len(parsed_lines.keys()))

def test_line_link():
    parsed_lines = parser.parse_lines(lines)
    assert_equal('http://www.wienerlinien.at/itip/linienwahl/linie.php?linie=1&', parsed_lines['1'])

def test_line_links():
    parsed_lines = parser.parse_lines(lines)
    assert_true(filter(lambda x: x.startswith('http://'), parsed_lines.values()))

def test_stations_66A():
    st = parser.parse_stations(load_data('bus/66A_stations.htm'))
    assert_true(st.has_key(u'Liesing S'))
    assert_true(st.has_key(u'Reumannplatz U'))
    assert_equal(29, len(st.values()[0]))
    assert_equal(30, len(st.values()[1]))

def test_departures_U2_in_kuerze_6min():
    dep = parser.parse_departures(load_data('underground/U2_in_kuerze_6min.htm'))
    assert_equal(2, len(dep))
    assert_equal(0, dep[0]['time'])
    assert_equal(6, dep[1]['time'])
    assert_equal(u'Aspernstrasse', dep[0]['direction'])
    assert_equal(u'Karlsplatz', dep[0]['station'])

def test_departures_U2_3min_8min():
    dep = parser.parse_departures(load_data('underground/U2_3min_8min.htm'))
    assert_equal(2, len(dep))
    assert_equal(3, dep[0]['time'])
    assert_equal(8, dep[1]['time'])
    assert_equal(u'Aspernstrasse', dep[0]['direction'])
    assert_equal(u'Karlsplatz', dep[0]['station'])

def test_departures_lowfloor():
    dep = parser.parse_departures(load_data('tram/41_1min_11min_21min.htm'))
    assert_true(dep[0]['lowfloor'])
    assert_false(dep[1]['lowfloor'])
    assert_true(dep[2]['lowfloor'])

def test_error_page():
    errorpage = load_data('errorpage.html')
    dep = parser.parse_departures(errorpage)
    assert_equal(0, len(dep))

def test_no_departures():
    nodepartures = load_data('nodepartures.html')
    dep = parser.parse_departures(nodepartures)
    assert_equal(0, len(dep))

def test_bus_stations():
    st = parser.parse_stations(load_data('bus/66A_stations.htm'))
    assert_equal(2, len(st.keys()))
    assert_equal(29, len(st.values()[0]))
    assert_equal(30, len(st.values()[1]))

### departures_by_station

def test_departures_by_station():
    dep = parser.parse_departures_by_station(stationbased)
    # find all 34 departures
    assert_equal(34, len(dep))
    l = list(set(map(lambda x: x['line'], dep)))
    # there are 8 different lines
    assert_equal(8, len(l))
    assert_equal(u'Leopoldau', dep[0]['direction'])
    assert_equal(u'Karlsplatz', dep[0]['station'])

def test_departures_by_station_lowfloor():
    dep = parser.parse_departures_by_station(stationbased)
    assert_true(dep[0]['lowfloor'])
    assert_false(dep[14]['lowfloor'])

def test_departures_by_station_datetime():
    dep = parser.parse_departures_by_station(stationbased)
    assert_is_instance(dep[13]['time'], int)
    assert_is_instance(dep[14]['departure'], datetime)
    assert_equal(4, dep[3]['time'])
    assert_equal(2, dep[4]['time'])
    assert_equal(18, dep[13]['time'])
    assert_equal('59A', dep[-4]['line'])
    assert_equal('WLB', dep[-1]['line'])
    assert_equal(datetime(2000, 1, 1, 13, 5), dep[14]['departure'])
