from typing import List, Optional
from uuid import UUID

from sqlalchemy import Column, func, select, false, true
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField, col
from sqlmodel import Session, SQLModel

from service.business.domain.base import BasePersistenceManager
from service.business.domain.model.category import CategoryInfo
from service.business.domain.model.entity import EntityInfo
from service.business.domain.model.observer import (OBSERVER_TYPE,
                                                    ObserverData, ObserverInfo)
from service.business.domain.model.stats import StatsInfo
from service.business.domain.model.taxonomy import TaxonomyInfo
from service.common.db.base_entity_manager import BaseEntityManager
from service.common.utils import search_dict


class TenantConfig(SQLModel, table=True):
    __tablename__ = "tenant_config"

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    config_key: str
    config_value: dict = SqlField(default='{}', sa_column=Column(JSONB))


class TaxonomyEntity(SQLModel, table=True):
    __tablename__ = "config_taxonomy"
    # __table_args__ = {'extend_existing': True}

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    term: str
    keyword: str
    description: Optional[str]
    tags: Optional[List[str]]
    is_deleted: bool
    is_enabled: bool

    def convert_to_model(self) -> TaxonomyInfo:
        return TaxonomyInfo(
            identifier=self.identifier,
            term=self.term,
            keyword=self.keyword,
            description=self.description,
            tags=self.tags,
            is_enabled=self.is_enabled
        )


class CategoryEntity(SQLModel, table=True):
    __tablename__ = "config_category"
    # __table_args__ = {'extend_existing': True}

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    name: str
    is_enabled: bool
    is_deleted: bool

    def convert_to_model(self) -> CategoryInfo:
        return CategoryInfo(
            identifier=self.identifier,
            name=self.name,
            is_enabled=self.is_enabled,
        )


class Entity(SQLModel, table=True):
    __tablename__ = "config_entity"
    # __table_args__ = {'extend_existing': True}

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    name: str
    tags: Optional[List[str]]
    is_enabled: bool
    is_deleted: bool

    def convert_to_model(self) -> EntityInfo:
        return EntityInfo(
            identifier=self.identifier,
            name=self.name,
            tags=self.tags,
            is_enabled=self.is_enabled,
        )


class Observer(SQLModel, table=True):
    __tablename__ = "config_observer"
    # __table_args__ = {'extend_existing': True}

    identifier: Optional[UUID] = SqlField(default=None, primary_key=True)
    name: str
    type: int
    entity_id: UUID
    config_data: dict = SqlField(default='{}', sa_column=Column(JSONB))
    is_enabled: bool
    is_deleted: bool

    def convert_to_model(self, entity: Entity) -> ObserverInfo:
        data_json = self.config_data
        official_handle = next(search_dict(data_json, 'official_handle'), None)
        url = next(search_dict(data_json, 'url'), None)
        observer_type_str = OBSERVER_TYPE.get(self.type)
        return ObserverInfo(
            identifier=self.identifier,
            name=self.name,
            entity_id=self.entity_id,
            entity_name=entity.name if entity else '',
            is_enabled=self.is_enabled,
            type=observer_type_str,
            config_data=ObserverData(
                official_handle=official_handle,
                url=url
            )
        )


class BusinessDBManager(BasePersistenceManager, BaseEntityManager):
    # Entity Related API
    def get_all_entities(self, tenant_id: UUID, enabled: Optional[bool] = None) -> List[EntityInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            query = session.query(Entity).filter(
                Entity.is_deleted == false(),
            ).order_by(
                col(Entity.is_enabled).desc(),
                Entity.name
            )
            if enabled is not None:
                query = query.filter(
                    Entity.is_enabled == enabled
                )

            entities = query.all()

            if entities:
                return [entity.convert_to_model() for entity in entities]
            return []

    def get_entity(self, tenant_id: UUID, entity_id: UUID) -> Optional[EntityInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            entity = session.query(Entity).filter(
                Entity.identifier == entity_id,
                Entity.is_deleted == false(),
            ).first()
            if entity:
                return entity.convert_to_model()
            return None

    def enabled_entities_count(self, tenant_id: UUID) -> List[StatsInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:

            result_set = session.query(
                Entity.is_enabled,
                func.count(Entity.is_enabled)
            ).group_by(
                Entity.is_enabled
            ).filter(
                Entity.is_deleted == false(),
            ).all()
            total = 0
            tracked = 0
            for flag, count in result_set:
                total += int(count)
                if flag:
                    tracked = int(count)

            return [
                StatsInfo(name="Tracked", value=tracked),
                StatsInfo(name="Total", value=total)
            ]

    def update_entity_enable_state(self, tenant_id: UUID, entity_id: UUID, new_state: bool):
        with Session(self._get_tenant_engine(tenant_id)) as session:
            session.query(Entity).filter(
                Entity.identifier == entity_id,
                Entity.is_deleted == false(),
            ).update(
                {'is_enabled': new_state}
            )
            session.commit()

    # Observer Related API
    def get_all_observers(self, tenant_id: UUID, enabled: Optional[bool] = None) -> List[ObserverInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            query = session.query(Observer).filter(
                Observer.is_deleted == false(),
            ).order_by(
                col(Observer.is_enabled).desc(),
                Observer.entity_id,
                Observer.name
            )
            if enabled is not None:
                query = query.filter(
                    Observer.is_enabled == enabled
                )

            observers = query.all()
            if observers:
                return [
                    observer.convert_to_model(
                        self.get_entity(
                            tenant_id=tenant_id,
                            entity_id=observer.entity_id
                        )
                    )
                    for observer in observers
                ]
            return []

    def get_observer(self, tenant_id: UUID, observer_id: UUID) -> Optional[ObserverInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            observer = session.query(Observer).filter(
                Observer.identifier == observer_id,
                Observer.is_deleted == false(),
            ).first()
            if observer:
                return observer.convert_to_model(
                    self.get_entity(
                        tenant_id=tenant_id,
                        entity_id=observer.entity_id
                    )
                )
            return None

    def enabled_observers_count(self, tenant_id: UUID) -> List[StatsInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            total_count = session.query(
                func.count(Observer.is_enabled)
            ).filter(
                Observer.is_deleted == false(),
            ).first()

            total = total_count[0]  # type: ignore

            result_set = session.query(
                func.count(Observer.is_enabled)
            ).filter(
                Observer.entity_id == Entity.identifier,
                Observer.is_enabled == true(),
                Entity.is_enabled == true(),
                Entity.is_deleted == false(),
                Observer.is_deleted == false(),
            ).all()

            tracked = 0
            for count in result_set:
                tracked += count[0]

            return [
                StatsInfo(name="Tracked", value=tracked),
                StatsInfo(name="Total", value=total)
            ]

    def update_observer_enable_state(self, tenant_id: UUID, observer_id: UUID, new_state: bool):
        with Session(self._get_tenant_engine(tenant_id)) as session:
            session.query(Observer).filter(
                Observer.identifier == observer_id,
                Observer.is_deleted == false(),
            ).update(
                {'is_enabled': new_state}
            )
            session.commit()

    # Taxonomy Related API
    def get_taxonomy_data(self, tenant_id: UUID) -> List[TaxonomyInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            taxonomy_entities = session.query(TaxonomyEntity).filter(
                TaxonomyEntity.is_deleted == false(),
            )
            if taxonomy_entities:
                return [taxonomy_entity.convert_to_model() for taxonomy_entity in taxonomy_entities]
        return []

    def enabled_taxonomy_count(self, tenant_id: UUID) -> List[StatsInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:

            result_set = session.query(
                TaxonomyEntity.is_enabled,
                func.count(TaxonomyEntity.is_enabled)
            ).group_by(
                TaxonomyEntity.is_enabled
            ).filter(
                TaxonomyEntity.is_deleted == false(),
            ).all()
            total = 0
            tracked = 0
            for flag, count in result_set:
                total += int(count)
                if flag:
                    tracked = int(count)

            return [
                StatsInfo(name="Tracked", value=tracked),
                StatsInfo(name="Total", value=total)
            ]

    def get_categories(self, tenant_id: UUID) -> List[CategoryInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            category_entities = session.query(CategoryEntity).filter(
                CategoryEntity.is_deleted == false(),
            )
            if category_entities:
                return [category_entity.convert_to_model() for category_entity in category_entities]
        return []

    def enabled_categories_count(self, tenant_id: UUID) -> List[StatsInfo]:
        with Session(self._get_tenant_engine(tenant_id)) as session:

            result_set = session.query(
                CategoryEntity.is_enabled,
                func.count(CategoryEntity.is_enabled)
            ).group_by(
                CategoryEntity.is_enabled
            ).filter(
                CategoryEntity.is_deleted == false(),
            ).all()
            total = 0
            tracked = 0
            for flag, count in result_set:
                total += int(count)
                if flag:
                    tracked = int(count)

            return [
                StatsInfo(name="Tracked", value=tracked),
                StatsInfo(name="Total", value=total)
            ]

    def get_dashboards(self, tenant_id: UUID) -> List[dict]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            query = select(TenantConfig).filter(TenantConfig.config_key == "dashboard_info")
            return self._execute_query(session, query)[0].config_value or []

    def get_panels(self, tenant_id) -> Optional[dict]:
        with Session(self._get_tenant_engine(tenant_id)) as session:
            query = select(TenantConfig).filter(TenantConfig.config_key == "panel_info")
            configs = self._execute_query(session, query)
            if len(configs) > 1:
                return configs[0].config_value
            else:
                return None
