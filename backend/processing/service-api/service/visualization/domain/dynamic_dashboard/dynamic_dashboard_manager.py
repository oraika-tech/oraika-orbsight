import logging
from typing import List, Optional
from uuid import UUID

from pydantic import BaseSettings

from service.visualization.domain.base import BasePersistenceManager
from service.visualization.domain.dynamic_dashboard.data_view_manager import DataViewManager
from service.visualization.domain.dynamic_dashboard.handler.chart_handler import handle_chart
from service.visualization.domain.dynamic_dashboard.handler.filter_panel_handler import handle_filter_panel
from service.visualization.domain.dynamic_dashboard.handler.live_feed_handler import handle_live_feed
from service.visualization.domain.dynamic_dashboard.handler.number_card_handler import handle_number_card
from service.visualization.domain.dynamic_dashboard.handler.simple_table_handler import handle_simple_table
from service.visualization.domain.model.chart_models import FilterDO, ChartDBO
from service.visualization.domain.model.dashboard_models import DashboardDO, FieldValue, Component

logger = logging.getLogger(__name__)


class DynamicDashboardManager(BaseSettings):
    persistence_manager: BasePersistenceManager
    data_view_manager: DataViewManager

    @staticmethod
    def get_field_element(component_inputs: List[FieldValue], field_name: str):
        for input_obj in component_inputs:
            if input_obj.field == field_name:
                return input_obj
        return None

    def get_field_value(self, component_inputs: List[FieldValue], field_name: str):
        element = self.get_field_element(component_inputs, field_name)
        return element.value if element else None

    def get_all_components_type(self,
                                components: Optional[List[Component]],
                                components_by_type: Optional[dict[str, list[Component]]] = None):

        if not components:
            return []

        if not components_by_type:
            components_by_type = {}

        for component in components:
            if component.type not in components_by_type:
                components_by_type[component.type] = []
            components_by_type[component.type].append(component)
            self.get_all_components_type(component.components, components_by_type)

        return components_by_type

    def get_updated_dashboard_info(self, tenant_id: UUID, tenant_code: str, dashboard: DashboardDO,
                                   filter_list: List[FilterDO], include_components: bool):
        if not include_components:
            dashboard.component_layout = None
            return dashboard

        if not dashboard.component_layout or len(dashboard.component_layout.components) == 0:
            return dashboard

        dashboard.component_layout.components = [component
                                                 for component in dashboard.component_layout.components
                                                 if not component.disabled]

        # section for batch processing by type
        charts = {}
        components_type_wise = self.get_all_components_type(dashboard.component_layout.components)
        for component_type, component_list in components_type_wise.items():
            if component_type == 'chart':
                chart_ids = [component.identifier
                             for component in component_list
                             if component.identifier]
                charts = self.persistence_manager.get_charts_by_ids(tenant_id, chart_ids)

        # section for single processing by type
        for component in dashboard.component_layout.components:
            self.handle_components(component, charts, tenant_code, filter_list)

        return dashboard

    def handle_grid(self, component, charts, tenant_code, filter_list):
        for child_component in component.components:
            self.handle_components(child_component, charts, tenant_code, filter_list)

    def handle_components(self, component: Component, charts: dict[UUID, ChartDBO],
                          tenant_code: str, filter_list: List[FilterDO]):
        if not component.inputs:
            component.inputs = []
        if component.type == 'chart':
            if component.identifier:
                handle_chart(self.data_view_manager,
                             component.inputs,
                             filter_list,
                             tenant_code,
                             charts[component.identifier])
        elif component.type == 'react-component':
            if component.name == 'FilterPanel':
                handle_filter_panel(self.data_view_manager, component.inputs, filter_list, tenant_code)
            elif component.name == 'LiveFeedTable':
                handle_live_feed(self.data_view_manager, component.inputs, filter_list, tenant_code)
            elif component.name == 'SimpleTable':
                handle_simple_table(self.data_view_manager, component.inputs, filter_list, tenant_code)
            elif component.name == 'StatsCard':
                handle_number_card(self.data_view_manager, component.inputs, filter_list, tenant_code)
            elif component.name == 'Grid':
                self.handle_grid(component, charts, tenant_code, filter_list)
