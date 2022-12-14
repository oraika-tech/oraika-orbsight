#!/usr/bin/env bash

DB_NAME=$1

echo "Start: $(date)"

source "$HOME/.orbsight/env"

if [[ "$DEMO_CRON_ENABLED" != 'true' ]]; then
  echo "Exit: $(date)"
  exit 0
fi

DB_USER=${DB_USER_RW:-orbsight}
DB_PASSWORD=${DB_PASSWORD_RW:-orbsight}
DB_HOST=${DB_HOST:-localhost:5432}
PERIOD_DAYS=29


SQL_QUERY="
UPDATE insight_raw_data
SET event_time = event_time + INTERVAL '$PERIOD_DAYS DAYS'
WHERE identifier IN (
	SELECT identifier
	FROM insight_raw_data
	WHERE event_time < NOW() - INTERVAL '$PERIOD_DAYS DAYS'
)
"

psql -t postgresql://"$DB_USER":"$DB_PASSWORD"@"$DB_HOST"/"$DB_NAME" <<<"$SQL_QUERY"

echo "End: $(date)"
