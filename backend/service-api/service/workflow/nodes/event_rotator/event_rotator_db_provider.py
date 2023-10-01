from uuid import UUID

from service.common.infra.db.repository.data.raw_data_repository import rotate_event_time


def rotate_event_time_dp(tenant_id: UUID, period_days: int):
    rotate_event_time(tenant_id, period_days)
