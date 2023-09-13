import unittest

from analyzer.service.utils import extract_json


class MyTestCase(unittest.TestCase):

    def test_extract_json(self):
        # Test case 1: Valid JSON array in the input text
        input_text = 'Json output:\n [\n {\n "id": 1,\n "sentiment": "positive",\n "tags": ["book"]\n }\n ]\nFew output'
        output_text = '[\n {\n "id": 1,\n "sentiment": "positive",\n "tags": ["book"]\n }\n ]'
        self.assertEqual(extract_json(input_text), output_text)

        # Test case 2: Valid JSON object in the input text
        input_text = 'Json output{ "id": 1,"sentiment": "positive","tags": ["booking", "maintenance"] }Future of world'
        output_text = '{ "id": 1,"sentiment": "positive","tags": ["booking", "maintenance"] }'
        self.assertEqual(extract_json(input_text), output_text)

        # Test case 3: No JSON in the input text
        input_text = "This is a text string without any JSON."
        self.assertEqual(extract_json(input_text), "No JSON start found in the input text")

        # Test case 4: Invalid JSON in the input text
        input_text = 'Json output{ "id": 1, "sentiment": "positive", "tags": ["booking", "maintenance", "waiting" }'
        self.assertEqual(extract_json(input_text), "No valid JSON found in the input text")

        # Test case 5: JSON at the start of the input text
        input_text = '[ { "sentiment": "positive", "tags": ["waiting"] } ] This is the end of the JSON output.'
        output_text = '[ { "sentiment": "positive", "tags": ["waiting"] } ]'
        self.assertEqual(extract_json(input_text), output_text)

        # Test case 6: JSON at the end of the input text
        input_text = 'JSON output. { "id": 1, "sentiment": "positive", "tags": ["booking", "maintenance", "waiting"] }'
        output_text = '{ "id": 1, "sentiment": "positive", "tags": ["booking", "maintenance", "waiting"] }'
        self.assertEqual(extract_json(input_text), output_text)


if __name__ == '__main__':
    unittest.main()
