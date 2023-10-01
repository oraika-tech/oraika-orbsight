import os
import unittest

from service.common.utils.utils import merge_dict_arrays_comp


class TestSegregateTagsTerms(unittest.TestCase):

    def setUp(self) -> None:
        self.data = {
            'department_list': ['Product', 'Engineering', 'HR', 'Finance'],
            'department_sublist': {
                'Product': ["Search", "Mail", "AdSense"],
                'Engineering': ["Data", "Platform", "QA"]
            }
        }
        self.data['activities'] = merge_dict_arrays_comp(self.data['department_sublist'])
        os.environ['OPENAI_API_KEY'] = 'test_value'

    def test_normal_case(self):
        classification_response = {
            'raw_data_id': 1,
            'departments': ['HR', 'Data']
        }

        from service.workflow.nodes.analyzer.text_analysis import segregate_tags_terms
        result = segregate_tags_terms(self.data, classification_response)

        self.assertEqual(result.tags, ['HR', 'Engineering'])
        self.assertEqual(result.terms, ['Data'])

    def test_empty_departments(self):
        classification_response = {
            'raw_data_id': 1,
            'departments': []
        }

        from service.workflow.nodes.analyzer.text_analysis import segregate_tags_terms
        result = segregate_tags_terms(self.data, classification_response)

        self.assertEqual(result.tags, [])
        self.assertEqual(result.terms, [])

    def test_no_intersection(self):
        classification_response = {
            'raw_data_id': 1,
            'departments': ['Marketing']
        }

        from service.workflow.nodes.analyzer.text_analysis import segregate_tags_terms
        result = segregate_tags_terms(self.data, classification_response)

        self.assertEqual(result.tags, [])
        self.assertEqual(result.terms, [])

    def test_sublist_intersection(self):
        classification_response = {
            'raw_data_id': 1,
            'departments': ['HR', 'Product', 'Mail']
        }

        from service.workflow.nodes.analyzer.text_analysis import segregate_tags_terms
        result = segregate_tags_terms(self.data, classification_response)

        self.assertEqual(result.tags, ['HR', 'Product'])
        self.assertEqual(result.terms, ['Mail'])


if __name__ == '__main__':
    unittest.main()
