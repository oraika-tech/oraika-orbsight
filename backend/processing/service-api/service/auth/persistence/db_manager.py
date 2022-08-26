from typing import Optional, Any, List

import bcrypt
from pydantic import Field, PrivateAttr
from sqlmodel import Field as SqlField, create_engine, Session, SQLModel

from service.auth.domain.base import BasePersistenceManager
from service.common.model.user import UserInfo


class EmployeeTable(SQLModel, table=True):
    __tablename__ = "employee"
    __table_args__ = {'extend_existing': True}

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    name: str
    email: str
    company_id: int
    role_ids: List[int]


class UserTable(SQLModel, table=True):
    __tablename__ = "user_auth"
    __table_args__ = {'extend_existing': True}

    identifier: Optional[int] = SqlField(default=None, primary_key=True)
    login_name: str
    hash_password: str
    employee_id: int
    is_deleted: bool


class UserDBManager(BasePersistenceManager):
    _engine: Any = PrivateAttr()

    db_host: str = Field("localhost:5432", env='DB_HOST')
    db_name: str = Field("orbsight_company", env='USER_DB_NAME')
    db_user: str = Field("orbsight", env='USER_DB_USER')
    db_password: str = Field("orbsight", env='USER_DB_PASSWORD')
    db_engine_name: str = Field("postgresql", env="DB_ENGINE_NAME")

    def __init__(self, **values: Any):
        super().__init__(**values)
        connection_string = f"{self.db_engine_name}://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"
        self._engine = create_engine(connection_string)

    def verify_user(self, login_name: str, password: str) -> Optional[int]:
        with Session(self._engine) as session:
            user_entity = session.query(UserTable).filter(
                UserTable.is_deleted == False,
                UserTable.login_name == login_name
            ).first()

            if user_entity is not None:
                if bcrypt.checkpw(password.encode(), user_entity.hash_password.encode()):
                    return user_entity.identifier

    def get_user(self, user_id: int) -> Optional[UserInfo]:
        with Session(self._engine) as session:
            user_entity, employee_entity = session.query(UserTable, EmployeeTable).filter(
                UserTable.identifier == user_id,
                UserTable.employee_id == EmployeeTable.identifier,
                UserTable.is_deleted == False,
            ).first()

            if user_entity is not None and employee_entity is not None:
                return UserInfo(
                    name=employee_entity.name,
                    company_id=employee_entity.company_id,
                    employee_id=employee_entity.identifier,
                    user_id=user_entity.identifier,
                    role_ids=employee_entity.role_ids or []
                )
