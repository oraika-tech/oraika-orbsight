#!/usr/bin/env bash

# Migration script naming
# https://flywaydb.org/documentation/concepts/migrations.html#naming

# default values for local dev
DB_USER=${DB_USER:-obsights}
DB_PASSWORD=${DB_PASSWORD:-obsights}
DB_HOST=${DB_HOST:-localhost:5432}
FLYWAY_EXECUTABLE=${FLYWAY_EXECUTABLE:-flyway}
# https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
# https://jonlabelle.com/snippets/view/shell/assigning-default-values-to-variables-in-bash

DIR_PATH=$(pwd)/$(dirname "$0")

function flyway_migrate() {
  FOLDER=$1
  DB_NAME=$2
  $FLYWAY_EXECUTABLE \
    -locations="filesystem:$DIR_PATH/../../$FOLDER,filesystem:$DIR_PATH/../../common" \
    -url="jdbc:postgresql://$DB_HOST/$DB_NAME" \
    -user="$DB_USER" \
    -password="$DB_PASSWORD" \
    migrate
}

flyway_migrate business obsights_business
flyway_migrate processing obsights_rbi
flyway_migrate company obsights_company
