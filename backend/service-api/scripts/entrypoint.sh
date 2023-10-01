#!/bin/bash

# Export the database connection URL
export PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://${PREFECT_DB_USER}:${PREFECT_DB_PASSWORD}@${DB_HOST}/${PREFECT_DB_NAME}"

# Start Prefect server
prefect server start &

# Start Gunicorn
gunicorn service.app.main:app -b 0.0.0.0:${SERVER_PORT} -k ${WORKER_TYPE} --workers ${NUM_OF_WORKERS} --timeout ${WORKER_TIMEOUT} --keep-alive ${KEEP_ALIVE} &

# Start Python Workflow
python service/workflow/workflow.py &

# Wait for all background jobs to finish
wait
