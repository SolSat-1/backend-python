from datetime import datetime
from pytz import timezone
from config.constants import TIMEZONE_UTC, TIMEZONE_THAI

UTC = timezone(TIMEZONE_UTC)
TH = timezone(TIMEZONE_THAI)


def now():
    return datetime.now(UTC)


def to_utc(dt):
    return dt.astimezone(UTC)


def to_local(dt, tz):
    return dt.astimezone(timezone(tz))


def to_string(dt, fmt="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(fmt)


def from_string(s, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(s, fmt).replace(tzinfo=UTC)


def from_timestamp(ts):
    return datetime.fromtimestamp(ts, UTC)


def to_timestamp(dt):
    return int(dt.timestamp())


def to_thai_string(dt, fmt="%Y-%m-%d %H:%M:%S"):
    return to_string(to_local(dt, TH), fmt)


def from_thai_string(s, fmt="%Y-%m-%d %H:%M:%S"):
    return from_string(s, fmt).astimezone(UTC)


def to_thai_datetime(dt):
    return to_local(dt, TH)
