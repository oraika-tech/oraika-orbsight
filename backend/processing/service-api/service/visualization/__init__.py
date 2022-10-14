from service.visualization.domain.data_view_manager import DataViewManager
from service.visualization.domain.domain_handler import VisualizationDomainHandler
from service.visualization.domain.dynamic_dashboard_manager import DynamicDashboardManager
from service.visualization.persistence.cubejs_client import CubejsClient
from service.visualization.persistence.db_manager import VisualizationDBManager

cubejs_client = CubejsClient()
visualization_db_manager = VisualizationDBManager()
data_view_manager = DataViewManager(cubejs_client=cubejs_client)
dynamic_dashboard_manager = DynamicDashboardManager(persistence_manager=visualization_db_manager,
                                                    data_view_manager=data_view_manager)
domain_handler = VisualizationDomainHandler(persistence_manager=visualization_db_manager,
                                            dynamic_dashboard_manager=dynamic_dashboard_manager)
