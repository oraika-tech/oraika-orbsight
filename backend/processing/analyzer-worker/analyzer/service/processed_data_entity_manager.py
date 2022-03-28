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

            service=data_request.get_structured_data_of_list_type("service", None),
            payment=data_request.get_structured_data_of_list_type("payment", None),
            transfer=data_request.get_structured_data_of_list_type("transfer", None),
            account_type=data_request.get_structured_data_of_list_type("account type", None),
            card=data_request.get_structured_data_of_list_type("card", None),
            identification=data_request.get_structured_data_of_list_type("identification", None),
            security=data_request.get_structured_data_of_list_type("security", None),
            currency=data_request.get_structured_data_of_list_type("currency", None),
            stock_market=data_request.get_structured_data_of_list_type("stock market", None),
            loan=data_request.get_structured_data_of_list_type("loan", None),
            network=data_request.get_structured_data_of_list_type("network", None),

            emotion=data_request.get_structured_data_of_str_type("emotion", None),

            fraud=data_request.get_structured_data_of_bool_type("fraud", False),
            complaint=data_request.get_structured_data_of_bool_type("complaint", False),
            harassment=data_request.get_structured_data_of_bool_type("harassment", False),
            access=data_request.get_structured_data_of_bool_type("access", False),
            delay=data_request.get_structured_data_of_bool_type("delay", False),
            interface=data_request.get_structured_data_of_bool_type("interface", False),
            charges=data_request.get_structured_data_of_bool_type("charges", False),

            text_length=data_request.get_structured_data_of_int_type("text_length", None),
            text_lang=data_request.get_structured_data_of_str_type("charges", None),
            remark=data_request.get_structured_data_of_str_type("remark", None),

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
