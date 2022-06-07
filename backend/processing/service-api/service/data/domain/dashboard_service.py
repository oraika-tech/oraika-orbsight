from typing import List, Any, Dict

from pydantic import BaseSettings
from service.data.domain.model.dashboard_data import DashboardData


class DashboardService(BaseSettings):
    panel_dashboard: Dict[str, DashboardData] = {}

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.panel_dashboard = {
            'live-feed': DashboardData(
                title='Live Feed',
                link="https://metabase.obsights.com/public/dashboard/25f9ff80-62d8-45ff-8858-524275a7a51d#refresh=300"
            ),
            'entity-distribution': DashboardData(
                title='Entity Distribution',
                link='https://metabase.obsights.com/public/question/cd07b038-b80a-481a-82cb-68a762cb853b#refresh=300'
            )
        }

    @staticmethod
    def get_dashboards() -> List[DashboardData]:
        return [
            DashboardData(
                title='Leaderboard',
                link='https://metabase.obsights.com/public/dashboard/b4bb7f58-28b2-4dcb-8503-1fbc229c74fd'
                     '#refresh=60'
            ),
            DashboardData(
                title="Entity Comparison",
                link="https://metabase.obsights.com/public/dashboard/5b754ec2-b210-417a-966e-469d85cbabe7"
                     "?date_filter=past7days&category=fraud#refresh=300"
            ),
            DashboardData(
                title="Entity Analysis",
                link="https://metabase.obsights.com/public/dashboard/23e75808-2057-42e0-9949-0999e7422e0d"
                     "?entity_name=State%20Bank%20of%20India#refresh=300"
            ),
            DashboardData(
                title="Data Crunching",
                link="https://grafana.obsights.com/d/DDPElelnz/data-crunching?orgId=1&theme=light&refresh=5m"
            )
        ]

    def get_dashboard_panel_data(self, panel: str) -> DashboardData:
        return self.panel_dashboard[panel]
