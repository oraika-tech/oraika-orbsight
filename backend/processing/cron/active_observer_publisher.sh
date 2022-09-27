#!/usr/bin/env bash

# Todo: fetch enabled tenants from core db and iterate over it
TENANT_ID=$1
DB_NAME=$2

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

MSG_FILE=/tmp/observer_rows_$TENANT_ID.json

SQL_QUERY="
SELECT row_to_json(ob) FROM (
  SELECT '$TENANT_ID' as tenant_id,
         o.identifier as observer_identifier,
         o.type as observer_type,
         o.config_data->'url' as url,
         o.config_data->'queries' as query,
         o.config_data->'language' as language,
         o.config_data->'country' as country,
         o.config_data->'page_id' as page_id,
         o.config_data->'subreddit' as subreddit,
         '$LOOKUP_PERIOD' as lookup_period,
         CASE
         WHEN o.type = 1 THEN $TWITTER_LIMIT_COUNT
         WHEN o.type = 2 THEN $ANDROID_LIMIT_COUNT
         WHEN o.type = 3 THEN $IOS_LIMIT_COUNT
         ELSE $LIMIT_COUNT
         END as limit_count
 FROM config_observer o JOIN config_entity e on o.entity_id = e.identifier
 WHERE o.is_enabled = true and e.is_enabled = true
) as ob LIMIT 200 "

psql -t postgresql://"$DB_USER":"$DB_PASSWORD"@"$DB_HOST"/"$DB_NAME" <<<"$SQL_QUERY" |
  grep -v '^\s*$' | # remove empty lines
  sed 's/"/\\"/g' | # escape quotes inside message
  sed -E 's/\s*(.*observer_identifier\\":\\"([0-9a-z-]+).*)\s*/{"Id":"\2","MessageBody":"\1"}/' \
    >$MSG_FILE

MSG_PART_FILE=/tmp/rows_part_$TENANT_ID.json

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
    --queue-url https://sqs.eu-west-1.amazonaws.com/067668835856/prod-observer \
    --entries file://$MSG_PART_FILE

done

echo "End: $(date)"
