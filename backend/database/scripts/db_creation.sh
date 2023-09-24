#!/usr/bin/env bash

set -e

DB_NAME=$1
USER_NAME=${2:-$DB_USER}
USER_PASSWORD=${3:-$DB_PASSWORD}

if [ -z "$USER_PASSWORD" ]; then
  echo "Usage: $0 <db_name> <username> <password>" 
  exit 1
fi

if [[ $DB_NAME = "orb_tenant_" ]]; then
  echo "Invalid DB name: 'orb_'"
  exit 1
fi

ADMIN_DB_USER=${ADMIN_DB_USER:-postgres}
ADMIN_DB_PASSWORD=${ADMIN_DB_PASSWORD}
DB_HOST=${DB_HOST:-localhost:5432}

function psql_cli() {
  FILE_NAME=$1
  if [[ -z $ADMIN_DB_PASSWORD ]]; then
    psql postgresql://"$ADMIN_DB_USER"@"$DB_HOST"/postgres -f $FILE_NAME -W
  else
    psql postgresql://"$ADMIN_DB_USER":"$ADMIN_DB_PASSWORD"@"$DB_HOST"/postgres -f $FILE_NAME
  fi
}

function create_user() {
  USERNAME=$1
  PASSWORD=$2
  FILE_NAME=/tmp/create_user.sql
  echo "CREATE USER $USERNAME WITH encrypted password '$PASSWORD';" >$FILE_NAME
  echo "Creating user"
  psql_cli $FILE_NAME
}

function create_db() {
  DB_NAME=$1
  USERNAME=$2
  FILE_NAME=/tmp/create_db.sql
  {
    echo "CREATE DATABASE $DB_NAME OWNER $ADMIN_DB_USER ENCODING 'UTF8';"
    echo "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $USERNAME;"
  } > $FILE_NAME
  echo "Creating database"
  psql_cli $FILE_NAME
}

create_user $USER_NAME $USER_PASSWORD
create_db $DB_NAME $USER_NAME
