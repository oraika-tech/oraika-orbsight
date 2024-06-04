#!/usr/bin/env bash

SCRIPT_DIR="$(dirname "$0")"
source /Users/girish/programs/oraika-env/bin/activate
export PREFECT_SERVER_API_HOST=0.0.0.0
export APP_NAME=worker
export OUTSCRAPPER_API_KEY=somekey
cd $SCRIPT_DIR/..
python -m service.workflow.workflow
