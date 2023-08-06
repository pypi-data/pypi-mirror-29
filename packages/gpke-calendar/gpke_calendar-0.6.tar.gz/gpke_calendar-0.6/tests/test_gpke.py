from datetime import datetime

import pytest

from gpke_calendar.gpke_calendar import get_next_date


def test_old_date():
    date = datetime.strptime('1970-01-01', '%Y-%m-%d')
    with pytest.raises(ValueError):
        get_next_date(date, 9)


def test_newer_than_2049_date():
    date = datetime.strptime('2050-01-01', '%Y-%m-%d')
    with pytest.raises(ValueError):
        get_next_date(date, 9)


def test_no_date():
    with pytest.raises(ValueError):
        get_next_date(None, 9)
