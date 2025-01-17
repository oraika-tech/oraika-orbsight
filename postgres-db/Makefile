

ifndef postgres_db_dir
	postgres_db_dir=.
endif

include $(postgres_db_dir)/../.env
export

create-init-scripts:
	cd $(postgres_db_dir); \
	envsubst < db-scripts/01-init-database.sql > db-init/01-init-database.sql;



