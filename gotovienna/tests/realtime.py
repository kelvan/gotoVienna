# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_true, assert_false
import sys
import os
from datetime import time
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
DATAPATH = 'data'

from gotovienna.realtime import *

parser = ITipParser()

stationbased = open(os.path.join(DATAPATH, 'stationbased.html'), 'r').read()
line_station = open(os.path.join(DATAPATH, 'line_station.html'), 'r').read()
errorpage = open(os.path.join(DATAPATH, 'errorpage.html'), 'r').read()
nodepartures = open(os.path.join(DATAPATH, 'nodepartures.html'), 'r').read()
lines = open(os.path.join(DATAPATH, 'lines.html'), 'r').read()
stations1 = open(os.path.join(DATAPATH, 'stations1.html'), 'r').read()
stations2 = open(os.path.join(DATAPATH, 'stations2.html'), 'r').read()

parsed_lines = parser.parse_lines(lines)

def test_lines():
    assert_equal(dict, type(parsed_lines))
    assert_true(parsed_lines)

def test_line_amount():
    assert_equal(104, len(parsed_lines.keys()))

def test_line_link():
    assert_equal('http://www.wienerlinien.at/itip/linienwahl/linie.php?lng=de&lng=de&linie=1', parsed_lines['1'])

def test_line_links():
    assert_true(filter(lambda x: x.startswith('http://'), parsed_lines.values()))

def test_stations1():
    st1 = parser.parse_stations(stations1)
    assert_true(st1.has_key(u'Gersthof, Herbeckstraße'))
    assert_true(st1.has_key(u'Schottentor U'))
    assert_equal(14, len(st1[u'Gersthof, Herbeckstraße']))
    assert_equal(12, len(st1[u'Schottentor U']))

def test_stations2():
    st2 = parser.parse_stations(stations2)
    assert_true(st2.has_key(u'Stefan-Fadinger-Platz'))
    assert_true(st2.has_key(u'Prater Hauptallee'))
    assert_equal(31, len(st2[u'Stefan-Fadinger-Platz']))
    assert_equal(30, len(st2[u'Prater Hauptallee']))

def test_departures_by_station():
    dep = parser.parse_departures_by_station(stationbased)
    # find all 34 departures
    assert_equal(34, len(dep))
    l = list(set(map(lambda x: x['line'], dep)))
    # there are 8 different lines
    assert_equal(8, len(l))

def test_departures_by_station_lowfloor():
    dep = parser.parse_departures_by_station(stationbased)
    assert_true(dep[0]['lowfloor'])
    assert_false(dep[14]['lowfloor'])

def test_departures_by_station_datetime():
    dep = parser.parse_departures_by_station(stationbased)
    assert_equal(int, type(dep[13]['time']))
    assert_equal(time, type(dep[14]['time']))

def test_departures():
    dep = parser.parse_departures(line_station)

def test_error_page():
    dep = parser.parse_departures(errorpage)
    assert_equal(0, len(dep))

def test_no_departures():
    dep = parser.parse_departures(nodepartures)
    assert_equal(0, len(dep))
