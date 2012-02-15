from nose.tools import assert_equal, assert_is_instance
import sys
import os
from datetime import time, datetime

# bananas for the monkey
class datetime_static(datetime):
    @classmethod
    def now(cls):
        return datetime(2000, 1, 1, 11, 50)

from gotovienna import realtime
realtime.datetime = datetime_static
# </bananas>

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from gotovienna.realtime import Departure
from utils import sort_departures

departures = [Departure('U2', 'Karlsplatz', 'Aspernstrasse', time(13, 37), True),
              Departure('U1', 'Karlsplatz', 'Reumannplatz', time(12, 24), False),
              Departure('U4', 'Karlsplatz', 'Huetteldorf', time(11, 42), False),
              Departure('U4', 'Karlsplatz', 'Heiligenstadt', 5, True),
              Departure('U2', 'Karlsplatz', 'Aspernstrasse', time(13, 38), True)]

departures_sorted = [Departure('U4', 'Karlsplatz', 'Huetteldorf', time(11, 42), False),
                     Departure('U4', 'Karlsplatz', 'Heiligenstadt', 5, True),
                     Departure('U1', 'Karlsplatz', 'Reumannplatz', time(12, 24), False),
                     Departure('U2', 'Karlsplatz', 'Aspernstrasse', time(13, 37), True),
                     Departure('U2', 'Karlsplatz', 'Aspernstrasse', time(13, 38), True)]

def test_sort():
    assert_equal(departures_sorted, sort_departures(departures))

def test_atime():
    for dep in departures:
        assert_is_instance(dep['departure'], datetime)

def test_ftime():
    for dep in departures:
        assert_is_instance(dep['ftime'], str)

def test_deltatime():
    for dep in departures:
        assert_is_instance(dep['time'], int)
