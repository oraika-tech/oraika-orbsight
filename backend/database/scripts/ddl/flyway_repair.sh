#!/usr/bin/env bash

# default values for local dev
DB_USER=${DB_USER:-obsights}
DB_PASSWORD=${DB_PASSWORD:-obsights}
DB_HOST=${DB_HOST:-localhost:5432}
FLYWAY_EXECUTABLE=${FLYWAY_EXECUTABLE:-flyway}

DIR_PATH=$(pwd)/$(dirname "$0")

function flyway_repair() {
  FOLDER=$1
  DB_NAME=$2
  $FLYWAY_EXECUTABLE \
    -locations="filesystem:$DIR_PATH/../../$FOLDER,filesystem:$DIR_PATH/../../common" \
    -url="jdbc:postgresql://$DB_HOST/$DB_NAME" \
    -user="$DB_USER" \
    -password="$DB_PASSWORD" \
    repair
}

flyway_repair business obsights_business
flyway_repair processing obsights_rbi
flyway_repair company obsights_company
