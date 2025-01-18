# Database Makefile

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

ifndef db_dir
	db_dir=.
endif

include $(db_dir)/../../.env
export


# For all db-* target export db admin credentials - ADMIN_DB_USER, ADMIN_DB_PASSWORD

# Usage:
#	make db-create db_name=metabase username=abc password=123
#	make db-create tenant=core username=abc password=123
db-create:
	bash $(db_dir)/scripts/db_creation.sh $(db_name) $(username) $(password) && echo "Success"

db-init-core:
	bash $(db_dir)/scripts/init-core-db.sh

db-create-tenant:
	bash $(db_dir)/scripts/create-tenant-db-data.sh $(tenant) $(email) $(user) $(password)

# make db-sync-changelog tenant=core
# make db-sync-changelog tenant=rbi
db-sync-changelog:
	$(eval ws_dir=schema/orb_$(shell if [ "${tenant}" = "core" ]; then echo "core"; else echo "tenant"; fi))
	bash $(db_dir)/scripts/liquibase.sh $(ws_dir) $(db_name) changelog-sync

# make db-sync-schema tenant=core
# make db-sync-schema tenant=rbi
db-sync-schema:
	$(eval ws_dir=schema/orb_$(shell if [ "${tenant}" = "core" ]; then echo "core"; else echo "tenant"; fi))
	bash $(db_dir)/scripts/liquibase.sh $(ws_dir) $(db_name) update
	
# make db-pull-data tenant=core
# make db-pull-data tenant=rbi
db-pull-data:
	bash $(db_dir)/scripts/pull_tenant_csv.sh $(tenant)

# make db-sync-data tenant=core
# make db-sync-data tenant=rbi
db-sync-data:
	python3 $(db_dir)/scripts/fill_data_with_field.py
	bash $(db_dir)/scripts/liquibase.sh data/$(tenant) $(db_name) update
