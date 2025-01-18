# from prefect.client.schemas.schedules import CronSchedule
from prefect import serve
from service.app.auth.auth_db_provider import get_all_demo_tenants_dp
from service.common.utils import logger_utils
from service.workflow.infra.workflow_db_provider import get_all_enabled_tenants_dp
from service.workflow.nodes.analyzer.analyzer_workflow import analyzer_wf
from service.workflow.nodes.event_rotator.event_rotator_workflow import event_time_rotator_wf
from service.workflow.nodes.ner_people.ner_workflow import ner_wf
from service.workflow.nodes.observer.observer_workflow import observer_wf
from service.workflow.nodes.spacepulse.spacepulse_workflow import spacepulse_wf

logger = logger_utils.initialize_logger(__name__)


def workflow_agent():
    tenants = get_all_enabled_tenants_dp()
    demo_tenants = get_all_demo_tenants_dp()
    # work_pool_name = "ECS Workers"

    jobs = ([
        observer_wf.to_deployment(
            name=tenant.name + " - Observer",
            # schedule=CronSchedule(cron="0 1 * * *", timezone="Asia/Kolkata"),
            # work_pool_name=work_pool_name,
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
            # schedule=CronSchedule(cron="15 1 * * *", timezone="Asia/Kolkata"),
            # work_pool_name=work_pool_name,
            parameters={
                "tenant_id": tenant.identifier,
                "lookup_period": "3d",  # 3 tries
                "limit_count": 0
            }
        )
        for tenant in tenants
    ] + [
        spacepulse_wf.to_deployment(
            name=tenant.name + " - SpacePulse Push",
            # schedule=CronSchedule(cron="30 1 * * *", timezone="Asia/Kolkata"),
            # work_pool_name=work_pool_name,
            parameters={
                "tenant_id": tenant.identifier,
                "lookup_period": "1d",  # 1 try
            }
        )
        for tenant in tenants
    ] + [
        event_time_rotator_wf.to_deployment(
            name=tenant.name + ' - Event Time Rotator',
            # schedule=CronSchedule(cron="0 1 * * *", timezone='Asia/Kolkata'),
            # work_pool_name=work_pool_name,
            parameters={
                'tenant_id': tenant.identifier,
                'period_days': 30
            }
        )
        for tenant in demo_tenants
    ] + [
        ner_wf.to_deployment(
            name=tenant.name + " - NER",
            # work_pool_name=work_pool_name,
            parameters={
                "tenant_id": tenant.identifier,
                "lookup_period": "30d",  # 3 tries
                "limit_count": 0  # zero is infinity
            }
        )
        for tenant in tenants
    ])

    serve(*jobs)


if __name__ == "__main__":
    logger.info("STARTED...")
    workflow_agent()
    logger.info("ENDED...")

