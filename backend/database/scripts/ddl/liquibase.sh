#!/usr/bin/env bash

set -e

# Migration script naming

# default values for local dev
DB_USER=${DB_USER:-obsights}
DB_PASSWORD=${DB_PASSWORD:-obsights}
DB_HOST=${DB_HOST:-localhost:5432}
LIQUIBASE_EXECUTABLE=${LIQUIBASE_EXECUTABLE:-liquibase}
# https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
# https://jonlabelle.com/snippets/view/shell/assigning-default-values-to-variables-in-bash

DIR_PATH=$(pwd)/$(dirname "$0")

function liquibase_call() {
  DATABASE=$1
  CMD=$2
  case $CMD in
  drop-all)
    echo "Extremely dangerous operation, exiting !"
    exit 1
    ;;
  diff-snapshot)
    COMMAND="diff --reference-url=offline:postgresql?snapshot=db_snapshot.json"
    ;;
  take-snapshot)
    COMMAND="snapshot --snapshot-format=json --output-file=db_snapshot.json"
    ;;
  *)
    COMMAND="${@:2}"
    ;;
  esac
  SNAPSHOT_FILE=db_snapshot.json
  cd "$DIR_PATH/../../$DATABASE/liquibase"
  if ! [[ $CMD =~ diff|snapshot|snapshot|update|version ]]; then
    if [[ ! -f $SNAPSHOT_FILE ]]; then
      echo "Snapshot file not found. Please rectify !"
      exit 1
    fi
    OUTPUT=$(liquibase_call "$DATABASE" diff --reference-url='offline:postgresql?snapshot=db_snapshot.json' 2>/dev/null |
      grep -A 10000 'Product Version:' | grep -v 'Product Version:' | grep -v NONE | cat)
    if [[ -n "$OUTPUT" ]]; then
      printf '\n######## DB MISMATCH: NEED ATTENTION ################\n\n'
      echo "$OUTPUT"
      printf "\nFor details run:\nbash %s %s diff-snapshot\n" "$0" "$DATABASE"
      printf '\n#####################################################\n\n'
    fi
  fi
  $LIQUIBASE_EXECUTABLE \
    --url="jdbc:postgresql://$DB_HOST/obsights_$DATABASE" \
    --username="$DB_USER" \
    --password="$DB_PASSWORD" \
    $COMMAND
}

function main() {
  if [ $# -lt 2 ]; then
    echo "Usage: $0 {business|company|rbi} {update|history|take-snapshot|diff-snapshot|status|validate|changelog-sync}"
    exit 128
  fi
  liquibase_call "$@"
  echo "Done !!"
}

main "$@"
