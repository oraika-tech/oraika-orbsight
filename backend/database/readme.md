# Create DB Setup

## Steps to create initial DB
Each step might require few environment variables. Export them to override default values.

| Environment Variable  | Default Value  | Description               |
|:----------------------|:---------------|:--------------------------|
| **ADMIN_DB_USER**     | postgres       | admin username            |
| **ADMIN_DB_PASSWORD** | postgres       | admin password            |
| **DB_HOST**           | localhost:5432 | host and port             |
| **DB_USER**           | obsights       | user username             |
| **DB_PASSWORD**       | obsights       | user password             |
| **FLYWAY_EXECUTABLE** | flyway         | path of flyway executable |


1. Create user and DBs  
```shell
bash -x database/scripts/ddl/db_creation.sh
```
2. Create tables via flyway migration
```shell
bash database/scripts/ddl/flyway.sh migrate
```
3. Populate initial data
```shell
bash database/scripts/dml/data_populator.sh
```

Note: Each script is running individual commands for all DBs (business, company, processing). If only one DB operation is required then comment other DBs command and then run scripts.  

---------------------------------------------------------------------

## Clean DBs
To clean all database:
```shell
bash database/scripts/ddl/flyway.sh clean
```

Note: Proceed with extreme caution, this will delete all data.

---------------------------------------------------------------------

## Repair DB
Sometimes we need to change previous migration scripts to update comments or formatting. Migration will start failing after these changes. We will need to run repair to correct flyway history, mostly to update checksum.
```shell
bash database/scripts/ddl/flyway.sh repair
```

---------------------------------------------------------------------