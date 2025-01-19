# Obsight Mono Repo

Install docker and docker-compose before continuing.
Also, install python3 with bcrypt and psycopg2.

# Running Docker Compose

![Docker Compose Architecture](/docs/assets/docker-compose-architecture.png)

Assuming you are using postgres provided by docker compose.

## Setup Environment Variables
Before running anything setup environment variables in `.env` file.
If may leave it default if you don't want to change anything. 
Update postgres details if using your own postgres instance. If your postgres is not running on localhost, you may need to update `DB_HOST` in docker compose file.

## Setup Postgres Data

### 0. Run Postgres Docker if using default
Then run the following command to start postgres.
```
docker compose --profile postgres up
```
If you have your own postgres instance, you can skip this step.

### 1. Initialize database
```
make db-init-core
```

### 2. Create tables for core database
```
make db-sync-schema tenant=core
```

### 3. Create & initialize tenant database
```
make db-create-tenant tenant={tenant_name} email={user_email} user={username} password={password}
```

### 4. Create tenant db tables
```
make db-sync-schema tenant={tenant_name}
```

### 5. Insert sample data
 - Download provided tenant zip and unzip in folder
 - Insert data
```
psql -h localhost -p ${DB_PORT} -U ${ORBSIGHT_TENANT_USER} -d orb_tenat_{tenant_name} -f {path_to_file}
```

### 6. Stop Postgres
You may do ctrl-c to stop postgres. If still running, you can stop docker compose.
```
docker compose --profile postgres down
```

Note: For a fresh start, you may delete the postgres data and start over.
```
sudo rm -rf postgres-data
```

## Build Docker Images
```
docker compose --profile all build
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

