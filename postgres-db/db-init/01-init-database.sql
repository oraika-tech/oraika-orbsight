-- Prefect
CREATE DATABASE prefect_db;
CREATE USER prefect_user WITH ENCRYPTED PASSWORD 'prefect_password';
GRANT ALL PRIVILEGES ON DATABASE prefect_db TO prefect_user;

-- Core DB
CREATE DATABASE orb_core;
CREATE USER orbsight_core_user WITH ENCRYPTED PASSWORD 'orbsight_core_password';
GRANT ALL PRIVILEGES ON DATABASE orb_core TO orbsight_core_user;

-- Tenant
CREATE USER orbsight_tenant_user WITH ENCRYPTED PASSWORD 'orbsight_tenant_password';


