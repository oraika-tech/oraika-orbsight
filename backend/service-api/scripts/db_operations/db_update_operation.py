import json
import logging
import os
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import flag_modified
from sqlmodel import Session

from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.data.processed_data_repository import ProcessedDataEntity
from service.common.utils.utils import is_pascal_case, convert_to_pascal

#
# Prerequisite
# 1. ssh -fNL 5433:{DB_HOST}:5432 -i ~/.ssh/id_rsa_aws ec2-user@{JUMP_BOX}
# 2. export DB_HOST=localhost:5433
# 3. export CORE_DB_PASSWORD
#

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mapping_file = os.path.dirname(__file__) + "/name_mapping.json"
with open(mapping_file) as f:
    name_mappings: dict[str, Optional[str | list[str]]] = json.load(f)

for k, v in name_mappings.items():
    if isinstance(v, str) and k.lower() == v.lower():
        raise ValueError(f"Key and value same for name_mappings: {k}")


def get_name(name: str) -> Optional[str | list[str]]:
    if name:
        if name in name_mappings:
            return name_mappings[name]
        if not is_pascal_case(name):
            return convert_to_pascal(name)
    return name


def names_conversion(names: list[str]) -> list[str]:
    new_names = []
    for name in names:
        if name:
            new_name = get_name(name)
            if isinstance(new_name, list):
                new_names.extend(new_name)
            elif new_name:
                new_names.append(new_name)
    return new_names


def update_unprocessed_data(tenant_id: UUID):
    with Session(get_tenant_engine(tenant_id)) as session:
        existing_records = session.query(ProcessedDataEntity).filter(
            ProcessedDataEntity.raw_data_id >= 85
        ).all()

        for record in existing_records:
            if record.people:
                old_names = record.people
                record.people = names_conversion(record.people)
                if old_names != record.people:
                    flag_modified(record, "people")
                    logger.info("%d: %s => %s", record.identifier, old_names, record.people)

        session.commit()


def update_specific_data(tenant_id: UUID):
    with Session(get_tenant_engine(tenant_id)) as session:
        existing_record = session.query(ProcessedDataEntity).filter(
            ProcessedDataEntity.identifier == 4069
        ).first()

        # existing_record.people = ["abc"]
        flag_modified(existing_record, "people")

        session.commit()


playarena_id = UUID('02ddd60c-2d58-47cc-a445-275d8e621252')
playjuniors_id = UUID('b6d5a44a-4626-491a-8fc0-3a11344d97f7')

update_unprocessed_data(playjuniors_id)
# update_specific_data(playarena_id)
