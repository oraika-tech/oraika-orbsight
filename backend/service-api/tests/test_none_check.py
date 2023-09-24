import unittest


class MyTestCase(unittest.TestCase):

    def test_equality(self):
        """
            Test cases is to test equality of None, Empty and Value
        """

        var_none = None
        var_empty_string = ''
        var_empty_list = []
        var_empty_dict = {}
        var_filled_string = 'abc'
        var_filled_list = [1, 2, 3]
        var_filled_dict = {'a': 1, 'b': 2, 'c': 3}

        # Check for None value
        self.assertEqual(bool(var_none), bool(var_none is not None))
        self.assertNotEqual(bool(var_empty_string), bool(var_empty_string is not None))
        self.assertNotEqual(bool(var_empty_list), bool(var_empty_list is not None))
        self.assertNotEqual(bool(var_empty_dict), bool(var_empty_dict is not None))
        self.assertEqual(bool(var_filled_string), bool(var_filled_string is not None))
        self.assertEqual(bool(var_filled_list), bool(var_filled_dict is not None))
        self.assertEqual(bool(var_filled_dict), bool(var_filled_dict is not None))

        # empty string is zero length
        self.assertEqual(bool(var_empty_string != ''), bool(len(var_empty_string) > 0))
        self.assertEqual(bool(var_filled_string != ''), bool(len(var_filled_string) > 0))

        # Check for valid non-empty value
        self.assertEqual(bool(var_none), bool(var_none is not None and len(var_none) > 0))
        self.assertEqual(bool(var_empty_string), bool(var_empty_string is not None and len(var_empty_string) > 0))
        self.assertEqual(bool(var_empty_list), bool(var_empty_list is not None and len(var_empty_list) > 0))
        self.assertEqual(bool(var_empty_dict), bool(var_empty_dict is not None and len(var_empty_dict) > 0))
        self.assertEqual(bool(var_filled_string), bool(var_filled_string is not None and len(var_filled_string) > 0))
        self.assertEqual(bool(var_filled_list), bool(var_filled_list is not None and len(var_filled_list) > 0))
        self.assertEqual(bool(var_filled_dict), bool(var_filled_dict is not None and len(var_filled_dict) > 0))

        # Conclusion: "if value" is equivalent to "if value is not None and len(value) > 0", i.e. non-empty check.


if __name__ == '__main__':
    unittest.main()
