import unittest
from unittest.mock import patch, Mock
from uuid import UUID

from service.common.db.observer_entity_manager import ObserverEntityManager


class TestObserverEntityManager(unittest.TestCase):

    @patch('service.common.db.observer_entity_manager.Session')
    @patch('service.common.db.base_entity_manager.BaseEntityManager._get_tenant_engine')
    def test_get_observer_tasks(self, MockedGetTenantEngine, MockedSession):
        # Arrange
        mocked_session_instance = Mock()
        MockedSession.return_value.__enter__.return_value = mocked_session_instance

        mocked_engine = Mock()
        MockedGetTenantEngine.return_value = mocked_engine

        # Mock query and filter behavior
        mock_query = Mock()
        mocked_session_instance.query.return_value = mock_query
        mock_query.filter.return_value = mock_query
        mock_query.add_columns.return_value = mock_query
        mock_query.limit.return_value = mock_query

        # Mock query results
        mock_query.all.return_value = [
            {'identifier': 1, 'type': 'type1'},
            {'identifier': 2, 'type': 'type2'},
        ]

        tenant_id = UUID("12345678-1234-5678-1234-567812345678")
        manager = ObserverEntityManager()

        # Act
        results = manager.get_observer_tasks(tenant_id)

        # Assert
        MockedGetTenantEngine.assert_called_once_with(tenant_id)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['identifier'], 1)
        self.assertEqual(results[0]['type'], 'type1')
        self.assertEqual(results[1]['identifier'], 2)
        self.assertEqual(results[1]['type'], 'type2')


if __name__ == '__main__':
    unittest.main()
