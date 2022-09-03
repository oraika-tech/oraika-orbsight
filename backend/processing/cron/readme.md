# Cron Jobs

According to our design, we will be using cron to trigger data ingestion jobs.

## Steps to enable jobs

1. Create orbsight working directory

```shell
mkdir ~/.orbsight
```

2. Populate `env` file, it will be source in and will be used by script.

```shell
echo "export DB_HOST=prod-orbsight.cu4iby7ba2we.eu-west-1.rds.amazonaws.com:5432" > ~/.orbsight/env
echo "export OBSERVER_CRON_ENABLED=false" >> ~/.orbsight/env
```

| Environment Variable      | Default Value  | Description                                                           |
|:--------------------------|:---------------|:----------------------------------------------------------------------|
| **HOME**                  | ~              | user home directory path                                              |
| **OBSERVER_CRON_ENABLED** | false          | true/false Flag to enable/disable cron jobs Change values accordingly |
| **DB_HOST**               | localhost:5432 | host and port                                                         |
| **DB_USER**               | orbsight       | user username                                                         |
| **DB_PASSWORD**           | orbsight       | user password                                                         |
| **LOOKUP_PERIOD**         | 7m             | lookup period for observer                                            |

3. Copy crontab file to cron.d folder

```shell
sudo cp ~/orbsight/processing/cron/observer_messager_job.crontab /etc/cron.d/
```

Assuming project root at `~/orbsight`. Change paths accordingly if required.

Monitor logs at `~/.orbsight/observer_cron.log`

------------------------------------------------------------------------------

## Observer cron job

Example of published message:

```json
{
  "id": 362,
  "tenant_id": "230139f2-d5e4-4ecf-846f-27e741f833bc",
  "observer_type": 3,
  "entity_id": "c8ed828d-4604-425d-b57f-11ac0f7c3d48",
  "url": "https://apps.apple.com/in/app/paytm-upi-payments-recharge/id473941634"
}
```
