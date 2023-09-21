from datetime import datetime, timedelta
from typing import Any

import pytz
from dateutil import parser


def convert_to_local_time(input_date: Any) -> datetime:
    local_tz = pytz.timezone('Asia/Kolkata')

    if isinstance(input_date, datetime):
        if input_date.tzinfo is None:
            input_date = pytz.utc.localize(input_date)
        return input_date.astimezone(local_tz)

    elif isinstance(input_date, str):
        try:
            naive_dt = datetime.fromisoformat(input_date)
            utc_dt = pytz.utc.localize(naive_dt)
            return utc_dt.astimezone(local_tz)
        except ValueError:
            raise Exception("Invalid string format")

    elif isinstance(input_date, int) or isinstance(input_date, float):
        try:
            utc_dt = datetime.fromtimestamp(input_date, tz=pytz.utc)
            return utc_dt.astimezone(local_tz)
        except ValueError:
            raise Exception("Invalid timestamp")

    else:
        raise Exception("Unsupported type")


def iso_format_to_datetime(input_date):
    datetime_val = parser.isoparse(input_date)
    return datetime_val.astimezone(pytz.utc)


def datetime_to_iso_format(datetime_value: datetime):
    return datetime_value.isoformat()


def now():
    return datetime.now()


def get_period_datetime(period: str) -> datetime:
    current_time = datetime.now()
    unit = period[-1]
    value = int(period[:-1])

    if unit == 'm':
        delta = timedelta(minutes=value)
    elif unit == 'h':
        delta = timedelta(hours=value)
    elif unit == 'd':
        delta = timedelta(days=value)
    elif unit == 'w':
        delta = timedelta(weeks=value)
    else:
        raise ValueError("Invalid period format")

    return current_time - delta
