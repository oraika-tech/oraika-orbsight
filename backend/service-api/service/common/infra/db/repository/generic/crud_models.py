from typing import Type

from sqlalchemy import ForeignKey, Column
from sqlalchemy.dialects.postgresql import UUID as PSQL_UUID

from service.common.models import TableName


# Add models for overriding auto-detected entity models. Only add extra or override fields
def get_entity_models(base) -> dict[TableName, Type]:
    class ConfigObserver(base):
        __tablename__ = TableName.CONFIG_OBSERVER.value
        __table_args__ = {'extend_existing': True}

        entity_id = Column(PSQL_UUID, ForeignKey(TableName.CONFIG_ENTITY.value + '.identifier'))

    return {
        TableName.CONFIG_OBSERVER: ConfigObserver
    }
