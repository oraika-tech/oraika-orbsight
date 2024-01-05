from datetime import datetime
from typing import List, Optional
from uuid import UUID

from service.app.auth.auth_models import TenantInfo
from service.app.data.data_models import RawData
from service.common.infra.db.entity_manager.data_entity_manager import get_unprocessed_data
from service.common.infra.db.entity_manager.workflow_entity_manager import get_unsent_processed_data
from service.common.infra.db.repository.core.tenant_repository import get_all_enabled_tenants
from service.common.infra.db.repository.data.processed_data_repository import ProcessedDataEntity, insert_structured_data
from service.common.infra.db.repository.workflow.node_meta_repository import update_status, log_wf_error
from service.common.models import NodeMetaState
from service.common.utils.reflection_utils import convert_models
from service.common.utils.utils import dict_get
from service.workflow.nodes.analyzer.domain_models import StructuredData
from service.workflow.nodes.analyzer.text_analysis import Sentiment
from service.workflow.nodes.spacepulse.spacepulse_client import SpacePulsePostRequest


def get_unprocessed_data_dp(tenant_id: UUID, min_event_time: datetime, limit_count: int) -> List[RawData]:
    raw_data_entities = get_unprocessed_data(tenant_id, min_event_time, limit_count)
    return convert_models(raw_data_entities, RawData)


def get_unsent_processed_data_dp(tenant_id: UUID, min_event_time: datetime) -> List[SpacePulsePostRequest]:
    results = get_unsent_processed_data(tenant_id, min_event_time)
    return [
        SpacePulsePostRequest(
            id=raw_data.identifier,
            text=raw_data.raw_text,
            sentiment=processed_data.emotion,
            departments=processed_data.taxonomy_tags,
            activities=processed_data.taxonomy_terms,
            people=processed_data.people if processed_data.people else [],
            source="Google Reviews",
            link=dict_get(raw_data.unstructured_data, "review_link"),
            rating=dict_get(raw_data.unstructured_data, "review_rating"),
            timestamp=int(raw_data.event_time.timestamp()),
            owner_answer_timestamp=dict_get(raw_data.unstructured_data, "owner_answer_timestamp"),
            likes=dict_get(raw_data.unstructured_data, "review_likes")
        )
        for raw_data, processed_data in results
        if raw_data.identifier
    ]


def update_status_dp(tenant_id: UUID, raw_data_id: int, status: NodeMetaState):
    update_status(tenant_id, raw_data_id, status)


def log_wf_error_dp(tenant_id: UUID, raw_data_id: int, error_message: str):
    log_wf_error(tenant_id, raw_data_id, error_message)


def insert_structured_data_dp(tenant_id: UUID, structured_data: StructuredData) -> Optional[int]:
    data_entity = ProcessedDataEntity(
        raw_data_id=structured_data.raw_data_id,
        taxonomy_tags=structured_data.tags,
        taxonomy_terms=structured_data.terms,
        emotion=structured_data.emotion if structured_data.emotion else str(Sentiment.UNDETERMINED),
        categories=structured_data.categories if structured_data.categories else [],
        people=structured_data.people,
        text_length=structured_data.text_length,
        text_lang=structured_data.text_language,
        remark=structured_data.remark
    )
    return insert_structured_data(tenant_id, data_entity)


def get_all_enabled_tenants_dp() -> List[TenantInfo]:
    tenant_entities = get_all_enabled_tenants()
    return convert_models(tenant_entities, TenantInfo)
