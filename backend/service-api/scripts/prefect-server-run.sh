#!/usr/bin/env bash

if [[-z $PYTHON_VENV]]; then
    echo Undefined PYTHON_VENV
    exit 22
fi

source ${PYTHON_VENV}/bin/activate
export PREFECT_SERVER_API_HOST=0.0.0.0
export PREFECT_API_DATABASE_CONNECTION_URL="postgresql+asyncpg://girish:girish@localhost:5432/prefect_db"
prefect server start
