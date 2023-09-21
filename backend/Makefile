# Root Makefile

mypy-analyse:
	mypy processing

cron-deploy:
	bash -x processing/cron/cron_deploy.sh

# $(*_dir) variable are required by respective Makefile to resolve parent directory

svc_api_dir=processing/service-api
include $(svc_api_dir)/Makefile

db_dir=database_v2
include $(db_dir)/Makefile

tenant_onboarding_dir=lambda/tenant_onboarding
