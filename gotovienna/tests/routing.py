# -*- coding: utf-8 -*-

from nose.tools import assert_equal, assert_true, assert_false
from datetime import datetime

from gotovienna.routing import *
DATAPATH = os.path.join(os.path.dirname(__file__), 'data')

underground_routing = open(os.path.join(DATAPATH, 'underground_routing.html'), 'r').read()
underground_foot_routing = open(os.path.join(DATAPATH, 'underground_foot_routing.html'), 'r').read()
foot_routing = open(os.path.join(DATAPATH, 'foot_routing.html'), 'r').read()

def test_extract_city():
    assert_equal('Wien', extract_city('Börse, Wien'))
    assert_equal('Wien', extract_city('Börse'))

def test_extract_station():
    assert_equal(u'Börse', extract_station(u'Börse, Wien'))
    assert_equal(u'Börse', extract_station(u'Börse'))

def test_split_station():
    assert_equal((u'Börse', 'Wien'), split_station(u'Börse, Wien'))
    assert_equal((u'Börse', 'Wien'), split_station(u'Börse'))

def test_guess_location_type():
    assert_equal('address', guess_location_type(u'Rathausstraße 6'))
    assert_equal('stop', guess_location_type(u'Börse'))

def test_overview1():
    """ Normal distance
    """
    router = rParser(underground_routing)
    assert_equal(4, len(router.overview))
    assert_equal(1, router.overview[0]['change'])
    assert_equal(1.8, router.overview[0]['price'])
    assert_equal([datetime(2011, 12, 16, 15, 44),
                  datetime(2011, 12, 16, 16, 0)],
                 router.overview[0]['timespan'])

def test_overview2():
    """ Mixed routing short distance (EUR 0.9) and normal distance
    """
    router = rParser(underground_foot_routing)
    assert_equal(8, len(router.overview))
    assert_equal(1, router.overview[0]['change'])
    assert_equal(0, router.overview[1]['change'])
    assert_equal(1.8, router.overview[0]['price'])
    assert_equal(0.9, router.overview[1]['price'])
    assert_equal([datetime(2011, 12, 16, 15, 44),
                  datetime(2011, 12, 16, 15, 54)],
                 router.overview[0]['timespan'])
    assert_equal([datetime(2011, 12, 16, 15, 44),
                  datetime(2011, 12, 16, 15, 59)],
                 router.overview[1]['timespan'])

def test_overview3():
    """ Short distance, routing by foot
    """
    router = rParser(foot_routing)
    assert_equal(1, len(router.overview))
    assert_equal(0, router.overview[0]['change'])
    assert_equal(.0, router.overview[0]['price'])
    assert_equal([], router.overview[0]['timespan'])
