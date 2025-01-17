# Obsight Mono Repo

- frontend
- backend
    - api_layer
    - service_layer
    - db_schema
- src
    - db_schema
    - worker


Install docker and docker-compose before continuing.

# Running Docker Compose

Assuming you are using postgres provided by docker compose. 

## Setup Environment Variables
Before running anything setup environment variables in `.env` file.
If may leave it default if you don't want to change anything.

## Setup Docker Postgres

### 1. Run docker compose
If environment variables changed in `.env` file, run the following command to update `01-init-database.sql` file.
```
make create-init-scripts
```

Then run the following command to start postgres.
```
docker compose --profile postgres up
```
On first run, the docker compose will run the db-init script to create the databases and users.

If you have your own postgres instance, you can skip this step.
Run `db-init` scripts to create databases and users in your postgres instance.


### 2. Create tables for core database
```
make db-sync-schema tenant=core
```

----


### 3. Insert default data in core database
```
make db-insert-default-data
```

### 4. Create tables for tenant database
```
make db-sync-schema tenant=tenant
```

### 5. Insert default data in tenant database
```
make db-insert-default-data
```

### 6. Stop Postgres
```
docker compose --profile postgres down
```

## Running Docker Compose

```
docker compose --profile all up
```

Service is up and running. You can access following services:
* Orbsight UI: http://localhost:3000
* Prefect UI: http://localhost:4200
* Backend API: http://localhost:8080/docs
* Cubejs: http://localhost:4000
* Postgres: localhost:5432

