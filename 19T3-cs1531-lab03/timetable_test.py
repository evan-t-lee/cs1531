import pytest

from datetime import date, time, datetime
from timetable import timetable

def test_empty():
    assert timetable([], []) == []

def test_normal():
    assert timetable([date(2019,9,27), date(2019,9,30)], [time(14,10), time(10,30)]) == [datetime(2019,9,27,10,30), datetime(2019,9,27,14,10), datetime(2019,9,30,10,30), datetime(2019,9,30,14,10)]

def test_single():
    assert timetable([date(2016,9,16)], [time(12,23)]) == [datetime(2016,9,16,12,23)]

def test_single_date():
    assert timetable([date(2017,3,7)], [time(5,47), time(8,7), time(16,54)]) == [datetime(2017,3,7,5,47), datetime(2017,3,7,8,7), datetime(2017,3,7,16,54)]

def test_single_time():
    assert timetable([date(2017,6,29)], [time(16,35), time(19,30), time(3,0)]) == [datetime(2017,6,29,3,0), datetime(2017,6,29,16,35), datetime(2017,6,29,19,30)]