from typing import Optional, Any, List, Set, Dict

from pydantic import Field, PrivateAttr
from sqlalchemy import func, Column, distinct, select
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import Field as SqlField, create_engine, Session, SQLModel

from service.business.domain.base import BasePersistenceManager
from service.business.domain.model.entity import EntityInfo
from service.business.domain.model.stats import StatsInfo
from service.business.domain.model.observer import ObserverInfo, OBSERVER_TYPE, ObserverData
from service.business.domain.model.taxonomy import TaxonomyInfo

from service.common.utils import search_dict


class TaxonomyEntity(SQLModel, table=True):
    __tablename__ = "taxonomy"
    __table_args__ = {'extend_existing': True}

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    company_id: int
    term: str
    term_description: Optional[str]
    categories: Optional[List[str]]
    taxonomy_type: Optional[Dict[str, Any]] = SqlField(default='{}', sa_column=Column(JSONB))
    is_deleted: bool

    def convert_to_model(self) -> TaxonomyInfo:
        return TaxonomyInfo(
            term=self.term,
            term_description=self.term_description,
            issue_categories=self.categories,
            issue_mapping=list(self.taxonomy_type.keys())
        )


class Entity(SQLModel, table=True):
    __tablename__ = "entity"
    __table_args__ = {'extend_existing': True}

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    name: str
    simple_name: str
    city: Optional[str]
    country: Optional[str]
    regulated_type: Optional[List[str]]
    is_enabled: bool
    is_deleted: bool
    company_id: int

    def convert_to_model(self) -> EntityInfo:
        return EntityInfo(
            identifier=self.identifier,
            name=self.name,
            simple_name=self.simple_name,
            regulated_type=self.regulated_type,
            is_enabled=self.is_enabled,
            is_deleted=self.is_deleted,
            city=self.city,
            country=self.country,
            company_id=self.company_id
        )


class Observer(SQLModel, table=True):
    __tablename__ = "observer"
    __table_args__ = {'extend_existing': True}

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    name: str
    observer_type: int
    entity_id: int
    data: str
    is_enabled: bool
    is_deleted: bool
    company_id: int

    def convert_to_model(self, entity: Entity) -> ObserverInfo:
        data_json = self.data
        official_handle = next(search_dict(data_json, 'official_handle'), None)
        url = next(search_dict(data_json, 'url'), None)
        observer_type_str = OBSERVER_TYPE.get(self.observer_type)
        return ObserverInfo(
            identifier=self.identifier,
            name=self.name,
            entity_id=self.entity_id,
            entity_name=entity.simple_name,
            is_enabled=self.is_enabled,
            company_id=self.company_id,
            observer_type=observer_type_str,
            data=ObserverData(
                official_handle=official_handle,
                url=url
            )
        )


class BusinessDBManager(BasePersistenceManager):
    _terms: List[TaxonomyInfo] = PrivateAttr()
    db_host: Optional[str] = Field("localhost:5432", env='DB_HOST')
    db_name: str = Field("obsights_business", env='BUSINESS_DB_NAME')
    db_user: str = Field("postgres", env='BUSINESS_DB_USER')
    db_password: str = Field("studio", env='BUSINESS_DB_PASSWORD')
    db_engine_name: str = Field("postgresql", env="DB_ENGINE_NAME")

    engine: Any

    def __init__(self, **values: Any):
        super().__init__(**values)
        connection_string = f"{self.db_engine_name}://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        self.engine = create_engine(connection_string)

    # Entity Related API
    def get_all_entities(self, company_id: int, enabled: Optional[bool] = None) -> List[EntityInfo]:
        with Session(self.engine) as session:
            query = session.query(Entity).filter(
                Entity.company_id == company_id,
                Entity.is_deleted == False,
            ).order_by(
                Entity.is_enabled.desc(),
                Entity.simple_name
            )
            if enabled is not None:
                query = query.filter(
                    Entity.is_enabled == enabled
                )

            entities = query.all()

            if entities is not None:
                return [entity.convert_to_model() for entity in entities]
            return []

    def get_entity(self, company_id: int, entity_id: int) -> Optional[EntityInfo]:
        with Session(self.engine) as session:
            entity = session.query(Entity).filter(
                Entity.identifier == entity_id,
                Entity.company_id == company_id,
                Entity.is_deleted == False,
            ).first()
            if entity is not None:
                return entity.convert_to_model()
            return None

    def enabled_entities_count(self, company_id: int) -> List[StatsInfo]:
        with Session(self.engine) as session:
            stats: List[StatsInfo] = []

            result_set = session.query(
                Entity.is_enabled,
                func.count(Entity.is_enabled)
            ).group_by(
                Entity.is_enabled
            ).filter(
                Entity.company_id == company_id,
                Entity.is_deleted == False,
            ).all()
            total = 0
            for flag, count in result_set:
                total += int(count)
                if flag:
                    stats.append(StatsInfo(name="Tracked", value=int(count)))

            stats.append(StatsInfo(name="Total", value=total))
            return stats

    def entities_type_count(self, company_id: int) -> List[StatsInfo]:
        with Session(self.engine) as session:
            result_set = session.query(
                Entity.regulated_type,
                func.count(Entity.regulated_type)
            ).group_by(
                Entity.regulated_type
            ).filter(
                Entity.company_id == company_id,
                Entity.is_deleted == False,
            ).all()

            stats_dict: Dict[str, int] = {}
            for entity_types, count in result_set:
                for entity_type in entity_types:
                    stats_dict[entity_type] = stats_dict.get(entity_type, 0) + count
            stats = [StatsInfo(name=key, value=value) for key, value in stats_dict.items()]
            return stats

    def update_entity_enable_state(self, company_id: int, entity_id: int, new_state: bool):
        with Session(self.engine) as session:
            session.query(Entity).filter(
                Entity.identifier == entity_id,
                Entity.company_id == company_id,
                Entity.is_deleted == False,
            ).update(
                {'is_enabled': new_state}
            )
            session.commit()

    # Observer Related API
    def get_all_observers(self, company_id: int, enabled: Optional[bool] = None) -> List[ObserverInfo]:
        with Session(self.engine) as session:
            query = session.query(Observer).filter(
                Observer.company_id == company_id,
                Observer.is_deleted == False,
            ).order_by(
                Observer.is_enabled.desc(),
                Observer.entity_id,
                Observer.name
            )
            if enabled is not None:
                query = query.filter(
                    Observer.is_enabled == enabled
                )

            observers = query.all()
            if observers is not None:
                return [
                    observer.convert_to_model(
                        self.get_entity(
                            company_id=company_id,
                            entity_id=observer.entity_id
                        )
                    )
                    for observer in observers
                ]
            return []

    def get_observer(self, company_id: int, observer_id: int) -> Optional[ObserverInfo]:
        with Session(self.engine) as session:
            observer = session.query(Observer).filter(
                Observer.identifier == observer_id,
                Observer.company_id == company_id,
                Observer.is_deleted == False,
            ).first()
            if observer is not None:
                return observer.convert_to_model(
                    self.get_entity(
                        company_id=company_id,
                        entity_id=observer.entity_id
                    )
                )
            return None

    def enabled_observers_count(self, company_id: int) -> List[StatsInfo]:
        with Session(self.engine) as session:
            stats: List[StatsInfo] = []

            total_count = session.query(
                func.count(Observer.is_enabled)
            ).filter(
                Observer.company_id == company_id,
                Observer.is_deleted == False,
            ).first()

            for count in total_count:
                stats.append(StatsInfo(name="Total", value=count))

            result_set = session.query(
                Observer.is_enabled,
                func.count(Observer.is_enabled)
            ).group_by(
                Observer.is_enabled
            ).filter(
                Observer.company_id == company_id,
                Entity.company_id == company_id,
                Observer.entity_id == Entity.identifier,
                Entity.is_enabled == True,
                Entity.is_deleted == False,
                Observer.is_deleted == False,
            ).all()

            for flag, count in result_set:
                if flag:
                    stats.append(StatsInfo(name="Tracked", value=count))

            return stats

    def observer_type_count(self, company_id: int) -> List[StatsInfo]:
        with Session(self.engine) as session:
            result_set = session.query(
                Observer.observer_type,
                func.count(Observer.observer_type)
            ).group_by(
                Observer.observer_type
            ).filter(
                Observer.company_id == company_id,
                Observer.is_deleted == False,
            ).all()

            stats: List[StatsInfo] = []
            for observer_type, count in result_set:
                stats.append(StatsInfo(name=OBSERVER_TYPE.get(observer_type), value=count))

            return stats

    def update_observer_enable_state(self, company_id: int, observer_id: int, new_state: bool):
        with Session(self.engine) as session:
            session.query(Observer).filter(
                Observer.identifier == observer_id,
                Observer.company_id == company_id,
                Observer.is_deleted == False,
            ).update(
                {'is_enabled': new_state}
            )
            session.commit()

    # Taxonomy Related API
    def get_taxonomy_data(self, company_id: int) -> List[TaxonomyInfo]:
        with Session(self.engine) as session:
            taxonomy_entities = session.query(TaxonomyEntity).filter(
                TaxonomyEntity.company_id == company_id,
                TaxonomyEntity.is_deleted == False,
            )
            if taxonomy_entities is not None:
                return [taxonomy_entity.convert_to_model() for taxonomy_entity in taxonomy_entities]
        return []

    def taxonomy_count(self, company_id: int) -> List[StatsInfo]:
        count = 0
        with Session(self.engine) as session:
            count_data = session.query(
                func.count(TaxonomyEntity.identifier)
            ).filter(
                TaxonomyEntity.company_id == company_id,
                TaxonomyEntity.is_deleted == False,
            ).first()

            count = count_data[0]

        return [
            StatsInfo(name="Total", value=count),
            StatsInfo(name="Tracked", value=count)
        ]

    def get_categories(self, company_id: int) -> List[str]:
        categories: Set[str] = set()
        with Session(self.engine) as session:
            stmt = select(distinct(TaxonomyEntity.categories)).filter(
                TaxonomyEntity.is_deleted == False,
                TaxonomyEntity.company_id == company_id,
                TaxonomyEntity.categories != None
            )
            row_list = session.exec(stmt)

            if row_list is not None:
                for row in row_list:
                    categories.update(row[0])
        return list(categories)

    def categories_count(self, company_id: int) -> List[StatsInfo]:
        categories: List[str] = self.get_categories(company_id)
        return [
            StatsInfo(name="Total", value=len(categories)),
            StatsInfo(name="Tracked", value=len(categories))
        ]

    def taxonomy_types_count(self, company_id: int) -> List[StatsInfo]:
        taxonomy_types_freq: Dict[str, int] = {}
        with Session(self.engine) as session:
            stmt = select(distinct(TaxonomyEntity.taxonomy_type)).filter(
                TaxonomyEntity.is_deleted == False,
                TaxonomyEntity.company_id == company_id,
                TaxonomyEntity.taxonomy_type != None
            )
            row_list = session.exec(stmt)

            if row_list is not None:
                for row in row_list:
                    for taxonomy_type, val in row[0].items():
                        taxonomy_types_freq[taxonomy_type] = taxonomy_types_freq.get(taxonomy_type, 0) + 1

        return [
            StatsInfo(name=key, value=value)
            for key, value in taxonomy_types_freq.items()
            if key is not None and key != ""
        ]
