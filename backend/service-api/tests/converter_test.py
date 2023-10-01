import unittest
from typing import TypeVar
from uuid import UUID

from pydantic import BaseModel

from service.app.business.business_models import ObserverInfo
from service.common.infra.db.repository.business.observer_repository import ObserverEntity
from service.common.utils.reflection_utils import convert_models

T = TypeVar('T')


class MyTestCase(unittest.TestCase):

    def test_create_model_list(self):
        # Test Case 1: Basic Test with field mapping
        observer1 = ObserverEntity(identifier=None, name="Observer1", type=1,
                                   entity_id=UUID(int=1), config_data={"key": "value"},
                                   is_enabled=True, is_deleted=False)
        observer2 = ObserverEntity(identifier=None, name="Observer2", type=2,
                                   entity_id=UUID(int=2), config_data={"key": "value2"},
                                   is_enabled=False, is_deleted=False)

        input_list = [observer1, observer2]
        field_map = {'type': 'entity_name', 'config_data': 'config_data'}
        output_list = convert_models(input_list, ObserverInfo, field_map)

        self.assertEqual(2, len(output_list))
        self.assertEqual("Observer1", output_list[0].name)
        self.assertEqual('1', output_list[0].entity_name)

        # Test Case 2: Empty List
        empty_input = []
        empty_output = convert_models(empty_input, ObserverInfo)
        self.assertEqual(0, len(empty_output))

        # Test Case 3: Type Mismatch (Corner Case)
        class AnotherModel(BaseModel):
            id: int  # type: ignore
            name: str  # type: ignore

        another_model_instance = AnotherModel(id=1, name="Test")
        mixed_input = [observer1, another_model_instance]

        mixed_output = convert_models(mixed_input, ObserverInfo, field_map)
        self.assertEqual(1, len(mixed_output))  # only observer1 should be converted successfully


if __name__ == '__main__':
    unittest.main()
