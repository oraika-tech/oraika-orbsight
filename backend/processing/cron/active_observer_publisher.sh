#!/usr/bin/env bash

echo "Start: $(date)"

source "$HOME/.orbsight/env"

if [[ "$OBSERVER_CRON_ENABLED" != 'true' ]]; then
  echo "Exit: $(date)"
  exit 0
fi

DB_USER=${DB_USER:-orbsight}
DB_PASSWORD=${DB_PASSWORD:-orbsight}
DB_HOST=${DB_HOST:-localhost:5432}
LOOKUP_PERIOD=${LOOKUP_PERIOD:-7m}
TWITTER_LIMIT_COUNT=${TWITTER_LIMIT_COUNT:-100}
ANDROID_LIMIT_COUNT=${ANDROID_LIMIT_COUNT:-20}
IOS_LIMIT_COUNT=${IOS_LIMIT_COUNT:-100}
LIMIT_COUNT=${LIMIT_COUNT:-20}

MSG_FILE=/tmp/observer_rows.json

SQL_QUERY="
SELECT row_to_json(ob) FROM (
  SELECT o.company_id,
         o.identifier as observer_identifier, o.name as observer_name, o.observer_type, o.regulated_entity_type,
         e.identifier as entity_identifier, e.simple_name as entity_simple_name, e.regulated_type,
         o.data->'url' as app_url, o.data->'official_handle' as twitter_handle,
         '$LOOKUP_PERIOD' as lookup_period,
         CASE
         WHEN o.observer_type = 1 THEN $TWITTER_LIMIT_COUNT
         WHEN o.observer_type = 2 THEN $ANDROID_LIMIT_COUNT
         WHEN o.observer_type = 3 THEN $IOS_LIMIT_COUNT
         ELSE $LIMIT_COUNT
         END as limit_count,
         e.country as entity_country, e.city as entity_city
 FROM observer o JOIN entity e on o.entity_id = e.identifier
 WHERE o.is_enabled = true and e.is_enabled = true
) as ob LIMIT 200 "

psql -t postgresql://"$DB_USER":"$DB_PASSWORD"@"$DB_HOST"/orbsight_business <<<"$SQL_QUERY" |
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
