import logging
from typing import List, Optional
from uuid import UUID

from service.app.visualization import visualization_db_provider as db_provider
from service.app.visualization.dynamic_dashboard.handler.chart_handler import handle_chart
from service.app.visualization.dynamic_dashboard.handler.filter_panel_handler import handle_filter_panel
from service.app.visualization.dynamic_dashboard.handler.key_phrases_handler import handle_key_phrases
from service.app.visualization.dynamic_dashboard.handler.live_feed_handler import handle_live_feed
from service.app.visualization.dynamic_dashboard.handler.number_card_handler import handle_number_card
from service.app.visualization.dynamic_dashboard.handler.simple_table_handler import handle_simple_table
from service.app.visualization.dynamic_dashboard.handler.word_cloud_handler import handle_word_cloud
from service.app.visualization.model.chart_models import FilterDO, ChartDBO
from service.app.visualization.model.dashboard_models import DashboardDO
from service.common.models import Component

logger = logging.getLogger(__name__)


def get_all_components_type(components: Optional[List[Component]],
                            components_by_type: Optional[dict[str, list[Component]]] = None):
    if not components:
        return []

    if not components_by_type:
        components_by_type = {}

    for component in components:
        if component.type not in components_by_type:
            components_by_type[component.type] = []
        components_by_type[component.type].append(component)
        get_all_components_type(component.components, components_by_type)

    return components_by_type


def get_updated_dashboard_info(tenant_id: UUID, tenant_code: str, dashboard: DashboardDO,
                               filter_list: List[FilterDO], include_components: bool):
    if not include_components:
        dashboard.component_layout = None
        return dashboard

    if not dashboard.component_layout or len(dashboard.component_layout.components) == 0:
        return dashboard

    dashboard.component_layout.components = [component
                                             for component in dashboard.component_layout.components
                                             if not component.disabled]

    # section for batch src by type
    chart_map_by_id = {}
    components_type_wise = get_all_components_type(dashboard.component_layout.components)
    for component_type, component_list in components_type_wise.items():
        if component_type == 'chart':
            chart_ids = [component.identifier
                         for component in component_list
                         if component.identifier]
            charts = db_provider.get_charts_dp(tenant_id, chart_ids)
            chart_map_by_id = {chart.identifier: chart for chart in charts if chart.identifier}

    # section for single src by type
    for component in dashboard.component_layout.components:
        handle_components(component, chart_map_by_id, tenant_code, filter_list)

    return dashboard


def handle_grid(component, charts, tenant_code, filter_list):
    grid_children = [child for child in component.components if child.disabled is not True]
    component.components = grid_children
    for child_component in component.components:
        handle_components(child_component, charts, tenant_code, filter_list)


def handle_components(component: Component, charts: dict[UUID, ChartDBO],
                      tenant_code: str, filter_list: List[FilterDO]):
    if not component.inputs:
        component.inputs = []
    if component.type == 'chart':
        if component.identifier:
            handle_chart(component.inputs,
                         filter_list,
                         tenant_code,
                         charts[component.identifier])
    elif component.type == 'react-component':
        if component.name == 'FilterPanel':
            handle_filter_panel(component.inputs, filter_list, tenant_code)
        elif component.name == 'LiveFeedTable':
            handle_live_feed(component.inputs, filter_list, tenant_code)
        elif component.name == 'KeyPhrasesPanel':
            handle_key_phrases(component.inputs, filter_list, tenant_code)
        elif component.name == 'WordCloudPanel':
            handle_word_cloud(component.inputs, filter_list, tenant_code)
        elif component.name == 'SimpleTable':
            handle_simple_table(component.inputs, filter_list, tenant_code)
        elif component.name == 'StatsCard':
            handle_number_card(component.inputs, filter_list, tenant_code)
        elif component.name == 'Grid':
            handle_grid(component, charts, tenant_code, filter_list)
