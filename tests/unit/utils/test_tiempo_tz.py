from app.utils.tiempo_tz import to_localtime, get_time_now
from datetime import datetime

def test_to_localtime_with_utc():
    dt = datetime(2023, 1, 1, 12, 0, 0)
    local_dt = to_localtime(dt)
    assert local_dt.tzinfo is not None

def test_get_time_now():
    now = get_time_now()
    assert isinstance(now, datetime)
    assert now.tzinfo is not None
