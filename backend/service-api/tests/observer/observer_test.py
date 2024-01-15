import json
from uuid import UUID

from service.workflow.nodes.observer.executor.base_executor import ObserverType, ObserverJobData
from service.workflow.nodes.observer.observer_workflow import fetch_data

job = ObserverJobData(
    tenant_id=UUID('9487b73b-5e2a-4839-ba12-02a63d473d5e'),
    observer_id=UUID('ea877dfb-f248-40a2-b03f-2ec61afb2c72'),
    observer_type=ObserverType.GoogleSearch,
    query='india maldives'
)

data_list = fetch_data(job)

print("Data: ", json.dumps([data.model_dump() for data in data_list]))
