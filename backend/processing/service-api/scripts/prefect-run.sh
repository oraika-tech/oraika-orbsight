#!/usr/bin/env bash

source /Users/girish/programs/oraika-env-3.11/bin/activate
export PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://girish:girish@localhost:5432/prefect_db"
prefect server start
