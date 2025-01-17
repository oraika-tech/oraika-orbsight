#!/bin/bash
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
  INSERT INTO my_table (name) VALUES ('example');
EOSQL
