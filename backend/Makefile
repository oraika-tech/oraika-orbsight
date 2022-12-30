# Root Makefile

mypy-analyse:
	mypy processing

cron-deploy:
	bash -x processing/cron/cron_deploy.sh

# $(*_dir) variable are required by respective Makefile to resolve parent directory

svc_api_dir=processing/service-api
include processing/service-api/Makefile

svc_analyzer_dir=processing/analyzer-worker
include processing/analyzer-worker/Makefile

svc_observer_dir=processing/observer-worker
include processing/observer-worker/Makefile

db_dir=database_v2
include database_v2/Makefile
