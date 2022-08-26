# Create DB Setup

## Steps to create initial DB
Each step might require few environment variables. Export them to override default values.

| Environment Variable  | Default Value  | Description               |
|:----------------------|:---------------|:--------------------------|
| **ADMIN_DB_USER**     | postgres       | admin username            |
| **ADMIN_DB_PASSWORD** | postgres       | admin password            |
| **DB_HOST**           | localhost:5432 | host and port             |
| **DB_USER**           | obsight        | user username             |
| **DB_PASSWORD**       | obsight        | user password             |
| **FLYWAY_EXECUTABLE** | flyway         | path of flyway executable |

Setup Liquibase using official page - [Installing Liquibase](https://docs.liquibase.com/install/home.html)
For each of database (business, company & rbi), we need to follow given steps.

1. Create user and DBs. This will create for all three DBs
```shell
bash -x database/scripts/ddl/db_creation.sh
```

2. Create tables and populate initial data via liquibase update
```shell
bash database/scripts/ddl/liquibase.sh <database> update
```

## Liquibase changeset scan order
Liquibase scan changeset in following order
* In the order of changeset in root changeset file
* In the order of include/includeAll statement
* For includeAll, in the lexicographical ordering of files in directory

## Liquibase Operations

Extensive list of commands are given in [liquibase commands](https://docs.liquibase.com/commands/home.html). Following are few frequently used commands.

Get help about liquibase command and options.
```shell
bash database/scripts/ddl/liquibase.sh <database> --help
```

Check migration status. If there is any mismatch between remote and snapshot then, it will be printed in output
```shell
bash database/scripts/ddl/liquibase.sh <database> status --verbose
```

Run migration via liquibase update
```shell
bash database/scripts/ddl/liquibase.sh <database> update
```

If changes are done in database not via liquibase, and they are consistent with migration script then you may just run sync
```shell
bash database/scripts/ddl/liquibase.sh <database> changelog-sync
```

If there is any file change which doesn't impact definition of db, like comments changes then resync checksum
```shell
bash database/scripts/ddl/liquibase.sh <database> clear-checksums
bash database/scripts/ddl/liquibase.sh <database> changelog-sync
```

Check diff between database and default snapshot
```shell
bash database/scripts/ddl/liquibase.sh <database> diff-snapshot
```

Check diff between database and reference snapshot
```shell
bash database/scripts/ddl/liquibase.sh <database> diff --reference-url='offline:postgresql?snapshot=db_snapshot.json'
```

Clean database to start fresh. EXTREMELY DANGEROUS. So not allowed in prod.
```shell
bash database/scripts/ddl/liquibase.sh <database> drop-all
```

Check execution history 
```shell
bash database/scripts/ddl/liquibase.sh <database> history
```

Each command take lock before running and release lock after completion.
In case earlier call failed or killed, you might need to release lock manually.
```shell
bash database/scripts/ddl/liquibase.sh <database> release-locks
```

[Rollback last x counts](https://docs.liquibase.com/commands/rollback/rollback-count.html).
```shell
bash database/scripts/ddl/liquibase.sh <database> rollback-count <count>
```

[Rollback up-to a given tag](https://docs.liquibase.com/commands/rollback/rollback-by-tag.html).
```shell
bash database/scripts/ddl/liquibase.sh <database> rollback --tag=<tag_name>
```

[Rollback to date](https://docs.liquibase.com/commands/rollback/rollback-to-date.html).
```shell
bash database/scripts/ddl/liquibase.sh <database> rollback-to-date 2020-05-07
```

Validate changelog for any potential issues.
```shell
bash database/scripts/ddl/liquibase.sh <database> validate
```

---------------------------------------------------------------------