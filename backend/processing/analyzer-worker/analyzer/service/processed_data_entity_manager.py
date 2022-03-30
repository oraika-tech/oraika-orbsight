from typing import Optional, List, Any

from pydantic import BaseSettings, Field
from sqlmodel import Field as SqlField, Session, SQLModel, create_engine

from analyzer.model.data_store_request import DBStoreRequest


class ProcessedDataEntity(SQLModel, table=True):
    __tablename__ = "processed_data"

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    company_id: int
    raw_data_id: int
    # Extraction from Text
    service: List[str]
    payment: List[str]
    transfer: List[str]
    account_type: List[str]
    card: List[str]
    identification: List[str]
    security: List[str]
    currency: List[str]
    stock_market: List[str]
    loan: List[str]
    network: List[str]
    # Extraction from AI model
    emotion: str
    fraud: bool
    complaint: bool
    harassment: bool
    access: bool
    delay: bool
    interface: bool
    charges: bool
    # Text Features
    text_length: int
    text_lang: str
    # Entity Info
    entity_name: str
    entity_type: str
    entity_country: str
    entity_city: str
    # Observer Info
    observer_name: str
    observer_type: str
    # To store some comment or un categories info
    remark: str


class ProcessedDataEntityManager(BaseSettings):
    db_host: Optional[str] = Field("localhost:5432", env='DB_HOST')
    db_name: str = Field("obsights_rbi", env='DB_NAME')
    db_user: str = Field("obsights", env='DB_USER')
    db_password: str = Field("obsights", env='DB_PASSWORD')
    engine: Any

    def __init__(self, **values: Any):
        super().__init__(**values)
        connection_string = f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        self.engine = create_engine(connection_string)

    def _snake_case(self, string: str, sep: str = ' ') -> str:
        words = [split_str.strip() for split_str in string.split(sep)]
        return "_".join(words)

    @staticmethod
    def convert_to_entity(data_request: DBStoreRequest):
        return ProcessedDataEntity(
            company_id=data_request.company_id,
            raw_data_id=data_request.raw_data_identifier,

            service=data_request.structured_data.entity_data.get("service", None),
            payment=data_request.structured_data.entity_data.get("payment", None),
            transfer=data_request.structured_data.entity_data.get("transfer", None),
            account_type=data_request.structured_data.entity_data.get("account type", None),
            card=data_request.structured_data.entity_data.get("card", None),
            identification=data_request.structured_data.entity_data.get("identification", None),
            security=data_request.structured_data.entity_data.get("security", None),
            currency=data_request.structured_data.entity_data.get("currency", None),
            stock_market=data_request.structured_data.entity_data.get("stock market", None),
            loan=data_request.structured_data.entity_data.get("loan", None),
            network=data_request.structured_data.entity_data.get("network", None),

            emotion=data_request.structured_data.emotion,

            fraud="fraud" in data_request.structured_data.categories,
            complaint="complaint" in data_request.structured_data.categories,
            harassment="harassment" in data_request.structured_data.categories,
            access="access" in data_request.structured_data.categories,
            delay="delay" in data_request.structured_data.categories,
            interface="interface" in data_request.structured_data.categories,
            charges="charges" in data_request.structured_data.categories,

            text_length=data_request.structured_data.text_length,
            text_lang=data_request.structured_data.text_language,
            remark=data_request.structured_data.remark,

            entity_name=data_request.entity_info.simple_name,
            entity_type=data_request.entity_info.type,
            entity_country=data_request.entity_info.country,
            entity_city=data_request.entity_info.city,

            observer_name=data_request.observer_info.name,
            observer_type=data_request.observer_info.type,
        )

    def insert_structure_data(self, data_request: DBStoreRequest) -> int:
        data_entity = self.convert_to_entity(data_request)
        with Session(self.engine) as session:
            session.add(data_entity)
            session.commit()
            session.refresh(data_entity)
            return data_entity.identifier
