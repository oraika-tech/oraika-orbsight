import logging

from prefect.client.schemas.schedules import CronSchedule
from prefect.runner import serve

from service.common.db.tenant_entity_manager import TenantEntityManager
from service.workflow.nodes.analyzer.analyzer_workflow import analyzer_wf
from service.workflow.nodes.event_rotator.event_rotator_workflow import event_time_rotator_wf
from service.workflow.nodes.observer.observer_workflow import observer_wf
from service.workflow.nodes.spacepulse.spacepulse_workflow import spacepulse_wf

# --------- Logging configuration ------------------------
# stop prefect verbose logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)
# --------- Logging configuration ------------------------

tenant_entity_manager = TenantEntityManager()


def workflow_agent():
    tenants = tenant_entity_manager.get_all_enabled_tenants()
    demo_tenants = tenant_entity_manager.get_all_demo_tenants()

    jobs = ([
                observer_wf.to_deployment(
                    name=tenant.name + " - Observer",
                    schedule=CronSchedule(cron="0 1 * * *", timezone="Asia/Kolkata"),
                    parameters={
                        "tenant_id": tenant.identifier,
                        "lookup_period": "28h",  # Keeping buffer of 3h
                        "limit_count": 300,
                    }
                )
                for tenant in tenants
            ] + [
                analyzer_wf.to_deployment(
                    name=tenant.name + " - Analyzer",
                    schedule=CronSchedule(cron="15 1 * * *", timezone="Asia/Kolkata"),
                    parameters={
                        "tenant_id": tenant.identifier,
                        "lookup_period": "3d",  # 3 tries
                    }
                )
                for tenant in tenants
            ] + [
                spacepulse_wf.to_deployment(
                    name=tenant.name + " - SpacePulse Push",
                    parameters={
                        "tenant_id": tenant.identifier,
                        "lookup_period": "3d",  # 3 tries
                    }
                )
                for tenant in tenants
            ] + [
                event_time_rotator_wf.to_deployment(
                    name=tenant.name + ' - Event Time Rotator',
                    schedule=CronSchedule(cron="0 1 * * *", timezone='Asia/Kolkata'),
                    parameters={
                        'tenant_id': tenant.identifier,
                        'period_days': 30
                    }
                )
                for tenant in demo_tenants
            ])

    serve(*jobs)


if __name__ == "__main__":
    logger.info("STARTED...")
    workflow_agent()
    logger.info("ENDED...")
