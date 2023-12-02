import unittest

from service.app.common.api_logger import get_body


class TestGetBodyFunction(unittest.TestCase):

    def test_empty_body(self):
        self.assertIsNone(get_body(b''))

    def test_valid_json_body(self):
        self.assertEqual(get_body(b'{"key": "value"}'), {"key": "value"})

    def test_invalid_json_body(self):
        self.assertEqual(get_body(b'{"key": "value'), {'wrong_body': '{"key": "value'})

    def test_non_json_body(self):
        self.assertEqual(get_body(b'plain text'), {'wrong_body': 'plain text'})

    def test_non_utf8_encoded_body(self):
        # This test might need adjustment based on how the function handles decoding errors
        self.assertIsNone(get_body(b'\xff\xd8\xff\xe0'))

    def test_json_body_with_utf8_special_characters(self):
        self.assertEqual(get_body(b'{"key": "\u00e9"}'), {"key": "\u00e9"})


if __name__ == '__main__':
    unittest.main()
