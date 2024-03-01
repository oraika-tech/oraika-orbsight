import json
import logging
import math
import os
import time
from typing import Optional
from uuid import UUID

import numpy as np
from service.common.infra.db.db_utils import get_tenant_engine
from service.common.infra.db.repository.data.processed_data_repository import ProcessedDataEntity
from service.common.utils.utils import convert_to_pascal_with_abbreviation, is_pascal_case
from sqlalchemy.orm.attributes import flag_modified
from sqlmodel import ARRAY, Session, String, cast, col, select

#
# Prerequisite
# 1. ssh -fNL 5433:{DB_HOST}:5432 -i ~/.ssh/id_rsa_aws ec2-user@{JUMP_BOX}
# 2. export DB_HOST=localhost:5433
# 3. export CORE_DB_PASSWORD
#

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mapping_file = os.path.dirname(__file__) + "/name_mapping.json"
with open(mapping_file, encoding='UTF-8') as f:
    name_mappings: dict[str, Optional[str | list[str]]] = json.load(f)

curr_names = list(name_mappings.keys())

for k, v in name_mappings.items():
    if isinstance(v, str) and k.lower() == v.lower():
        raise ValueError(f"Key and value same for name_mappings: {k}")


def get_name(name: str) -> Optional[str | list[str]]:
    if name:
        if name in name_mappings:
            return name_mappings[name]
        if not is_pascal_case(name):
            return convert_to_pascal_with_abbreviation(name)
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


def update_unprocessed_data(tenant_id: UUID, field_name: str, min_data_id: int):
    field_mapping = {
        'people': ProcessedDataEntity.people,
        'taxonomy_tags': ProcessedDataEntity.taxonomy_tags,
        'taxonomy_terms': ProcessedDataEntity.taxonomy_terms
    }
    if field_name not in field_mapping:
        logger.error("Wrong Argument: %s", field_name)
        return

    with Session(get_tenant_engine(tenant_id)) as session:
        existing_records = session.exec(
            select(ProcessedDataEntity)
            .where(
                ProcessedDataEntity.raw_data_id >= min_data_id,
                col(field_mapping[field_name]).overlap(cast(curr_names, ARRAY(String)))  # type: ignore[attr-defined]
            ).order_by(col(ProcessedDataEntity.identifier).desc())
        ).all()

        total_size = len(existing_records)
        batch_size = 100

        if total_size == 0:
            logger.info("No record found!")
            return

        sub_records = np.array_split(existing_records, math.ceil(total_size/batch_size))  # type: ignore
        i = 0

        initial_time = time.time()

        for records in sub_records:
            curr_time = time.time()
            avg_speed = i / (curr_time - initial_time) or 1
            time_left = int((total_size - i) / avg_speed)
            logger.info("Done %d out of %d with %d records/sec, time left: %d", i, total_size, avg_speed, time_left)
            i += 100
            for record in records:
                curr_field_value = getattr(record, field_name)
                if curr_field_value:
                    new_field_value = names_conversion(curr_field_value)
                    if curr_field_value != new_field_value:
                        setattr(record, field_name, new_field_value)
                        flag_modified(record, field_name)
                        logger.info("%d: %s => %s", record.identifier, curr_field_value, new_field_value)

            session.commit()


def update_specific_data(tenant_id: UUID, field_name: str, data_id: int):
    with Session(get_tenant_engine(tenant_id)) as session:
        existing_record = session.exec(
            select(ProcessedDataEntity)
            .where(ProcessedDataEntity.identifier == data_id)
        ).first()

        # existing_record.people = ["abc"]
        flag_modified(existing_record, field_name)

        session.commit()


playarena_id = UUID('02ddd60c-2d58-47cc-a445-275d8e621252')
playjuniors_id = UUID('b6d5a44a-4626-491a-8fc0-3a11344d97f7')

update_unprocessed_data(playarena_id, 'people', 1)
# update_specific_data(playarena_id, 'people', 1)
