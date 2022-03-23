#!/usr/bin/env bash

ADMIN_DB_USER=${ADMIN_DB_USER:-postgres}
ADMIN_DB_PASSWORD=${ADMIN_DB_PASSWORD:-postgres}
DB_HOST=${DB_HOST:-localhost:5432}

function create_user() {
  USERNAME=$1
  PASSWORD=$2
  FILE_NAME=/tmp/create_user.sql
  echo "CREATE USER $USERNAME WITH encrypted password '$PASSWORD';" >$FILE_NAME
  echo "GRANT pg_read_server_files TO $USERNAME;" >>$FILE_NAME
  psql postgresql://"$ADMIN_DB_USER":"$ADMIN_DB_PASSWORD"@"$DB_HOST" -f $FILE_NAME
}

function create_db() {
  DB_NAME=$1
  USERNAME=$2
  FILE_NAME=/tmp/create_db.sql
  echo "CREATE DATABASE $DB_NAME OWNER $USERNAME ENCODING 'UTF8';" >$FILE_NAME
  echo "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $USERNAME;" >>$FILE_NAME
  psql postgresql://"$ADMIN_DB_USER":"$ADMIN_DB_PASSWORD"@"$DB_HOST" -f $FILE_NAME
}

create_user obsights obsights
create_db obsights_business obsights
create_db obsights_company obsights
create_db obsights_rbi obsights
