# Cron Jobs

According to our design, we will be using cron to trigger data ingestion jobs.

# Steps to enable jobs

1. Create obsights working directory

```shell
mkdir ~/.obsights
```

2. Populate `env` file, it will be source in and will be used by script.

```shell
echo "export DB_HOST=10.0.1.167:5432" > ~/.obsights/env
echo "export OBSERVER_CRON_ENABLED=false" >> ~/.obsights/env
```

Variables:

* **DB_HOST**: Postgresql host
* **OBSERVER_CRON_ENABLED**: Flag to enable/disable cron jobs Change values accordingly.

3. Copy crontab file to cron.d folder

```shell
sudo cp ~/obsights/processing/cron/observer_messager_job.crontab /etc/cron.d/
```

Assuming project root at `~/obsights`. Change paths accordingly if required.

Monitor logs at `~/.obsights/observer_cron.log`

------------------------------------------------------------------------------

# Observer cron job

Example of published message:

```json
{
  "id": 362,
  "company_id": 1,
  "observer_type": 3,
  "entity_id": 111,
  "url": "https://apps.apple.com/in/app/paytm-upi-payments-recharge/id473941634"
}
```
