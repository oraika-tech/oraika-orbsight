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
    -locations="filesystem:$DIR_PATH/../../$FOLDER/flyway,filesystem:$DIR_PATH/../../common/flyway" \
    -url="jdbc:postgresql://$DB_HOST/$DB_NAME" \
    -user="$DB_USER" \
    -password="$DB_PASSWORD" \
    migrate
}

function flyway_clean() {
  DB_NAME=$1
  $FLYWAY_EXECUTABLE \
    -url="jdbc:postgresql://$DB_HOST/$DB_NAME" \
    -user="$DB_USER" \
    -password="$DB_PASSWORD" \
    clean
}

function flyway_repair() {
  FOLDER=$1
  DB_NAME=$2
  $FLYWAY_EXECUTABLE \
    -locations="filesystem:$DIR_PATH/../../$FOLDER/flyway,filesystem:$DIR_PATH/../../common/flyway" \
    -url="jdbc:postgresql://$DB_HOST/$DB_NAME" \
    -user="$DB_USER" \
    -password="$DB_PASSWORD" \
    repair
}

CMD=$1
MODULE=$2

case $MODULE in
  business)
    DB_NAME_ARG=obsights_business
    ;;
  company)
    DB_NAME_ARG=obsights_company
    ;;
  processing)
    DB_NAME_ARG=obsights_rbi
    ;;
  *)
    echo "Usage: $0 {migrate|clean|repair} {business|company|processing}"
    exit 128
esac


case $1 in
  migrate)
    flyway_migrate "$MODULE" $DB_NAME_ARG
  ;;
  clean)
    flyway_clean $DB_NAME_ARG
  ;;
  repair)
    flyway_repair "$MODULE" $DB_NAME_ARG
  ;;
  *)
    echo "Usage: $0 {migrate|clean|repair} {business|company|processing}"
    exit 128
esac

echo "Done !!"
