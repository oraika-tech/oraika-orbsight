import unittest
from datetime import datetime

import pytz

from service.common.utils.dateutils import convert_to_local_time


class TestConvertToLocalTime(unittest.TestCase):

    def test_datetime_utc(self):
        input_dt = datetime(2023, 9, 18, 14, 0, tzinfo=pytz.utc)
        output_dt = convert_to_local_time(input_dt)
        self.assertEqual(output_dt.tzinfo, pytz.timezone('Asia/Kolkata'))

    def test_datetime_naive(self):
        input_dt = datetime(2023, 9, 18, 14, 0)
        output_dt = convert_to_local_time(input_dt)
        self.assertEqual(output_dt.tzinfo, pytz.timezone('Asia/Kolkata'))

    def test_iso_string(self):
        input_str = "2023-09-18T14:00:00"
        output_dt = convert_to_local_time(input_str)
        self.assertEqual(output_dt.tzinfo, pytz.timezone('Asia/Kolkata'))

    def test_invalid_string(self):
        input_str = "invalid_string"
        output_dt = convert_to_local_time(input_str)
        self.assertEqual(output_dt, "Invalid string format")

    def test_timestamp(self):
        input_ts = 1695052654  # Corresponds to 2023-09-18T14:00:00 UTC
        output_dt = convert_to_local_time(input_ts)
        print("Datetime:", input_ts, type(input_ts), output_dt, output_dt.tzinfo, type(output_dt))
        self.assertEqual(output_dt.tzinfo, pytz.timezone('Asia/Kolkata'))

    def test_unsupported_type(self):
        input_list = [1, 2, 3]
        output_dt = convert_to_local_time(input_list)
        self.assertEqual(output_dt, "Unsupported type")


if __name__ == '__main__':
    unittest.main()
