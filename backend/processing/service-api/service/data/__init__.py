from service.data.persistence.db_manager import DataDBManager
from service.data.domain.domain_handler import DataDomainHandler

data_db_manager = DataDBManager()
data_domain_handler = DataDomainHandler(persistence_manager=data_db_manager)
