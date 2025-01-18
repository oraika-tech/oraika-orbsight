#!/bin/bash

DIR=$(dirname "$0")
source ${DIR}/../../../.env

# Create roles if they don't exist
psql postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:${DB_PORT}/postgres <<-EOSQL
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '${PREFECT_USER}') THEN
    CREATE ROLE ${PREFECT_USER} WITH LOGIN ENCRYPTED PASSWORD '${PREFECT_PASSWORD}' CREATEDB;
  END IF;
  
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '${ORBSIGHT_CORE_USER}') THEN
    CREATE ROLE ${ORBSIGHT_CORE_USER} WITH LOGIN ENCRYPTED PASSWORD '${ORBSIGHT_CORE_PASSWORD}' CREATEDB;
  END IF;
  
  IF NOT EXISTS (SELECT FROM pg_user WHERE usename = '${ORBSIGHT_TENANT_USER}') THEN
    CREATE ROLE ${ORBSIGHT_TENANT_USER} WITH LOGIN ENCRYPTED PASSWORD '${ORBSIGHT_TENANT_PASSWORD}' CREATEDB;
  END IF;
END
\$\$;
EOSQL

# Create prefect_db using prefect_user credentials
psql postgresql://${PREFECT_USER}:${PREFECT_PASSWORD}@localhost:${DB_PORT}/postgres <<-EOSQL
    CREATE DATABASE prefect_db;
EOSQL

# Create orb_core using orbsight_core_user credentials
psql postgresql://${ORBSIGHT_CORE_USER}:${ORBSIGHT_CORE_PASSWORD}@localhost:${DB_PORT}/postgres <<-EOSQL
    CREATE DATABASE orb_core;
EOSQL
