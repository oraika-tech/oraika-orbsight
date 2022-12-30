import datetime as datetime

import pytz
from dateutil import parser


def iso_format_to_datetime(input_date):
    datetime_val = parser.isoparse(input_date)
    return datetime_val.astimezone(pytz.utc)


def datetime_to_iso_format(datetime_value: datetime.datetime):
    return datetime_value.isoformat()
