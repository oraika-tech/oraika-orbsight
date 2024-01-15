import unittest

from service.common.utils.utils import hash_text


class TestHashText(unittest.TestCase):
    def test_hash_text_with_regular_string(self):
        self.assertEqual(hash_text("hello"), "LPJNul+wow4m6DsqxbninhsWHlwfp0JecwQzYpOLmCQ=")

    def test_hash_text_with_empty_string(self):
        self.assertEqual(hash_text(""), "47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=")

    def test_hash_text_with_special_characters(self):
        self.assertEqual(hash_text("@#$$%^&*()"), "0oMetxSu+WJVJg/g82038YMAcb/tRGcuqG5vSZduUG0=")

    def test_hash_text_with_unicode_characters(self):
        self.assertEqual(hash_text("こんにちは"), "Elrq3yewRZuHYME6PYCRLfqKgaaCYZBvYNh/SgJoZGw=")


if __name__ == '__main__':
    unittest.main()
