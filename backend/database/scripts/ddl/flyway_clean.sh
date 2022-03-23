#!/usr/bin/env bash

# default values for local dev
DB_USER=${DB_USER:-obsights}
DB_PASSWORD=${DB_PASSWORD:-obsights}
DB_HOST=localhost:${DB_HOST:-5432}
FLYWAY_EXECUTABLE=${FLYWAY_EXECUTABLE:-flyway}

function flyway_clean() {
  DB_NAME=$1
  $FLYWAY_EXECUTABLE \
    -url="jdbc:postgresql://$DB_HOST/$DB_NAME" \
    -user="$DB_USER" \
    -password="$DB_PASSWORD" \
    clean
}

flyway_clean obsights_business
flyway_clean obsights_rbi
flyway_clean obsights_company
