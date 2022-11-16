
#
# To use cli argument, pass them as {parameter}={argument}.
# e.g.
# make db-create-tenant tenant=core username=core password=core
#

ifeq ($(tenant),core)
	db_name=orb_core
else
	db_name=orb_tenant_$(tenant)
endif

port=8080

# For all db-* target export db admin credentials - ADMIN_DB_USER, ADMIN_DB_PASSWORD

# Usage:
#	make db-create db_name=metabase username=abc password=123
#	make db-create tenant=core username=abc password=123
db-create:
	bash database_v2/scripts/db_creation.sh $(db_name) $(username) $(password) && echo "Success"

# make db-sync-schema tenant=core
# make db-sync-schema tenant=rbi
db-sync-schema:
	$(eval ws_dir=schema/orb_$(shell if [ "${tenant}" = "core" ]; then echo "core"; else echo "tenant"; fi))
	bash database_v2/scripts/liquibase.sh $(ws_dir) $(db_name) update
	
# make db-pull-data tenant=core
# make db-pull-data tenant=rbi
db-pull-data:
	bash database_v2/scripts/pull_tenant_csv.sh $(tenant)

# make db-sync-data tenant=core
# make db-sync-data tenant=rbi
db-sync-data:
	bash database_v2/scripts/liquibase.sh data/$(tenant) $(db_name) update

# service commands

svc-observer-dep:
	cd processing/observer-worker; \
	pip install -e .

svc-observer-run:
	cd processing/observer-worker; \
	uvicorn observer.presentation.observer_job_controller:app --reload --port=$(port)

svc-analyzer-dep:
	cd processing/analyzer-worker; \
	pip install -e .

svc-analyzer-run:
	cd processing/analyzer-worker; \
	uvicorn analyzer.api.api:app --reload --port=$(port)

svc-api-compile:
	cd processing/service-api; \
	pip-compile --resolver=backtracking -U pyproject.toml

svc-api-dep:
	cd processing/service-api; \
	pip install -e .

svc-api-run:
	cd processing/service-api; \
	uvicorn service.main:app --reload --port=$(port)

svc-test:
	pytest processing/service-api/tests/test_*.py
