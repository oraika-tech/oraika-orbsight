from typing import List, Dict, Any
from uuid import UUID

from service.common.infra.db.entity_manager.business_entity_manager import get_observer_tasks


def get_observer_tasks_dp(tenant_id: UUID) -> List[Dict[Any, Any]]:
    return get_observer_tasks(tenant_id)
