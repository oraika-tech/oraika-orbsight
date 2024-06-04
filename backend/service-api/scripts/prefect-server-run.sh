#!/usr/bin/env bash

source /Users/girish/programs/oraika-env/bin/activate
export PREFECT_SERVER_API_HOST=0.0.0.0
export PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://girish:girish@localhost:5432/prefect_db"
prefect server start
