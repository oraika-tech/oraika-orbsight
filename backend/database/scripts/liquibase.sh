#!/usr/bin/env bash

set -e

# Migration script naming

# LIQUIBASE_EXECUTABLE=${LIQUIBASE_EXECUTABLE:-liquibase}
# https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
# https://jonlabelle.com/snippets/view/shell/assigning-default-values-to-variables-in-bash

DIR_PATH=$(pwd)/$(dirname "$0")

function liquibase_call() {
  WS_DIR=$1
  DATABASE=$2
  CMD=$3

  # default values for local dev
  DB_HOST=localhost:${DB_PORT}
  if [ "${DATABASE}" = "orb_core" ]; then
    DB_USER=${ORBSIGHT_CORE_USER}
    DB_PASSWORD=${ORBSIGHT_CORE_PASSWORD}
    LB_DIR=orb_core
  else
    DB_USER=${ORBSIGHT_TENANT_USER}
    DB_PASSWORD=${ORBSIGHT_TENANT_PASSWORD}
    LB_DIR=orb_tenant
  fi

  DB_USER=postgres
  DB_PASSWORD=postgres
  

  case $CMD in
  drop-all)
    echo "Extremely dangerous operation, do you want to continue !? (y/N) "
    read Y_OR_N
    if [ "$Y_OR_N" != 'Y' -a "$Y_OR_N" != 'y' ] ; then
      echo "Thought so :)"
      exit 1
    fi
    echo "Enter passcode: "
    read PASSCODE
    if [ $PASSCODE == 'delete_complete_database' ]; then
      COMMAND="drop-all"
    else
      echo "Wrong passcode, exiting..."
      exit 1
    fi
    ;;
  diff-snapshot)
    COMMAND="diff --reference-url=offline:postgresql?snapshot=db_snapshot.json"
    ;;
  take-snapshot)
    COMMAND="snapshot --snapshot-format=json --output-file=db_snapshot.json"
    ;;
  *)
    COMMAND="${@:3}"
    ;;
  esac

  SNAPSHOT_FILE=db_snapshot.json
  cd "$DIR_PATH/../$WS_DIR/.."
  if ! [[ $CMD =~ diff|snapshot|snapshot|changelog-sync|update|version|drop-all ]]; then
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
  set -x
  docker run --rm \
    --env-file ../../../.env \
    -v $(pwd):/liquibase/changelog \
    liquibase:4.30 \
      --driver=org.postgresql.Driver \
      --url="jdbc:postgresql://172.17.0.1:5433/${DATABASE}" \
      --username="$DB_USER" \
      --password="$DB_PASSWORD" \
      --changeLogFile=changelog/$LB_DIR/changelog-root.yml \
      --log-level=INFO \
      $COMMAND
  set +x
}

function main() {
  if [ $# -lt 2 ]; then
    echo "Usage: $0 {liquibase_directory} {db_name} {update|history|take-snapshot|diff-snapshot|status|validate|changelog-sync}"
    exit 128
  fi
  liquibase_call "$@"
  echo "Done !!"
}

main "$@"
