from typing import List, Dict, Any
from uuid import UUID

from sqlalchemy import true
from sqlalchemy.sql import label
from sqlmodel import Session

from service.business.persistence.db_manager import Observer, Entity
from service.common.db.base_entity_manager import BaseEntityManager


class ObserverEntityManager(BaseEntityManager):

    def get_observer_tasks(self, tenant_id: UUID) -> List[Dict[Any, Any]]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            query = session.query().filter(
                Observer.is_enabled == true(),
                Entity.is_enabled == true(),
                Observer.entity_id == Entity.identifier
            )

            query = query.add_columns(
                Observer.identifier,
                Observer.type,
                label("url", Observer.config_data["url"].astext if Observer.config_data is not None else None),
                label("query", Observer.config_data["query"].astext if Observer.config_data is not None else None),
                label("language", Observer.config_data["language"].astext if Observer.config_data is not None else None),
                label("country", Observer.config_data["country"].astext if Observer.config_data is not None else None),
                label("page_id", Observer.config_data["page_id"].astext if Observer.config_data is not None else None),
                label("subreddit", Observer.config_data["subreddit"].astext if Observer.config_data is not None else None),
            )

            results = query.limit(200).all()
            return results
