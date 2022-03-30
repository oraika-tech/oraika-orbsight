#!/usr/bin/env bash

echo "Start: $(date)"

source "$HOME/.obsights/env"

if [[ "$OBSERVER_CRON_ENABLED" != 'true' ]]; then
  echo "Exit: $(date)"
  exit 0
fi

DB_USER=${DB_USER:-obsights}
DB_PASSWORD=${DB_PASSWORD:-obsights}
DB_HOST=${DB_HOST:-localhost:5432}
LOOKUP_PERIOD=${LOOKUP_PERIOD:-7m}

MSG_FILE=/tmp/observer_rows.json

SQL_QUERY="
SELECT row_to_json(ob) FROM (
  SELECT o.company_id, o.identifier as observer_identifier, o.observer_type, o.name as observer_name,
         o.data->'url' as app_url, o.data->'official_handle' as twitter_handle,
         '$LOOKUP_PERIOD' as lookup_period,
         e.identifier as entity_identifier, e.simple_name as entity_simple_name,
         e.type as entity_type, e.country as entity_country, e.city as entity_city
 FROM observer o JOIN entity e on o.entity_id = e.identifier
 WHERE o.is_enabled = true and e.is_enabled = true
) as ob LIMIT 200 "

psql -t postgresql://"$DB_USER":"$DB_PASSWORD"@"$DB_HOST"/obsights_business <<<"$SQL_QUERY" |
  grep -v '^\s*$' | # remove empty lines
  sed 's/"/\\"/g' | # escape quotes inside message
  sed -E 's/\s*(.*observer_identifier\\":([0-9]+).*)\s*/{"Id":"\2","MessageBody":"\1"}/' \
    >$MSG_FILE

MSG_PART_FILE=/tmp/rows_part.json

cd /tmp/ || exit 1
split -l 10 --additional-suffix msg_part $MSG_FILE
for part_file in *msg_part*; do

  echo '[' >"$MSG_PART_FILE"
  sed -e '$ ! s/$/,/' "$part_file" >>"$MSG_PART_FILE"
  echo ']' >>"$MSG_PART_FILE"

  LINE_NOS=$(wc -l $MSG_PART_FILE | cut -d' ' -f1)

  if [[ $LINE_NOS -le 2 ]]; then
    echo "Error: $(date)"
    exit 1
  fi

  aws sqs send-message-batch \
    --queue-url https://sqs.eu-west-1.amazonaws.com/637364613199/prod-observer \
    --entries file://$MSG_PART_FILE

done

echo "End: $(date)"
