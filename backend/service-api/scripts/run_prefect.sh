#!/bin/bash

# Put this script in any machine to run prefect server and worker

SCRIPT_DIR="$(dirname "$0")"
echo "Running in directory: ${SCRIPT_DIR}"

export DB_HOST=${DB_HOST:-localhost:5432}
export PREFECT_DB_NAME=${PREFECT_DB_NAME:-prefect}
export PREFECT_DB_USER=${PREFECT_DB_USER:-prefect}
export PREFECT_DB_PASSWORD=${PREFECT_DB_PASSWORD:-prefect}
export PREFECT_SERVER_API_HOST=0.0.0.0
export PREFECT_API_URL="http://127.0.0.1:4200/api"

# Export the database connection URL
export PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://${PREFECT_DB_USER}:${PREFECT_DB_PASSWORD}@${DB_HOST}/${PREFECT_DB_NAME}"

# Start Prefect server
prefect server start 2>&1 >> ${SCRIPT_DIR}/prefect-server.log &
echo Started server...

# Delay for server to start
sleep 10

# Start work pool
prefect worker start --pool "ECS Workers" 2>&1 >> ${SCRIPT_DIR}/prefect-ecs-worker.log &
echo Started worker...
