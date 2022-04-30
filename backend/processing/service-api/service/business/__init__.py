from service.business.persistence.db_manager import BusinessDBManager
from service.business.domain.domain_handler import BusinessDomainHandler

business_db_manager = BusinessDBManager()
business_domain_handler = BusinessDomainHandler(persistence_manager=business_db_manager)
