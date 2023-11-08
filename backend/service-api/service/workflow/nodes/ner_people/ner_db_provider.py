from datetime import datetime
from uuid import UUID

from service.app.data.data_models import RawData
from service.common.infra.db.entity_manager.data_entity_manager import get_unprocessed_people_data, update_people_data
from service.common.utils.reflection_utils import convert_models
from service.workflow.nodes.analyzer.text_analysis import TextPeople


def get_unprocessed_ner_data(tenant_id: UUID, min_event_time: datetime, limit_count: int = 0) -> list[RawData]:
    raw_data_entities = get_unprocessed_people_data(tenant_id, min_event_time, limit_count)
    return convert_models(raw_data_entities, RawData)


def add_people_data(tenant_id: UUID, text_people_list: list[TextPeople]):
    people_list = [people.dict() for people in text_people_list]
    update_people_data(tenant_id, people_list)
