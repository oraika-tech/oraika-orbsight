from typing import Optional
from uuid import UUID

from service.common.infra.db.repository.business.config_repository import get_tenant_config
from service.common.utils.reflection_utils import convert_model
from service.workflow.nodes.spacepulse.spacepulse_client import SpacePulseTenantInfo


def get_space_pulse_tenant_info(tenant_id: UUID, config_key: str) -> Optional[SpacePulseTenantInfo]:
    tenant_config = get_tenant_config(tenant_id, config_key)
    return convert_model(tenant_config, SpacePulseTenantInfo)
