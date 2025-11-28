import pytest
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from app.utils.tiempo_tz import to_localtime, get_time_now


def test_to_localtime_with_utc():
    dt = datetime(2023, 1, 1, 12, 0, 0, tzinfo=ZoneInfo("UTC"))
    local_dt = to_localtime(dt)
    assert local_dt.tzinfo is not None
    assert isinstance(local_dt, datetime)


def test_to_localtime_without_tzinfo():
    dt = datetime(2023, 1, 1, 12, 0, 0)
    local_dt = to_localtime(dt)
    assert local_dt.tzinfo is not None


def test_to_localtime_none():
    assert to_localtime(None) is None


def test_get_time_now():
    now = get_time_now()
    assert isinstance(now, datetime)
    assert now.tzinfo is not None
