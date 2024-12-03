#!/usr/bin/env bash

if [[-z $PYTHON_VENV]]; then
    echo Undefined PYTHON_VENV
    exit 22
fi

SCRIPT_DIR="$(dirname "$0")"
source ${PYTHON_VENV}/bin/activate
# export PREFECT_SERVER_API_HOST=0.0.0.0
export PREFECT_API_URL=http://127.0.0.1:4200/api
export APP_NAME=worker
# export OUTSCRAPPER_API_KEY=somekey
# export OPENAI_API_KEY=somekey
cd $SCRIPT_DIR/..
python -m service.workflow.workflow
