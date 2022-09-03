# Observer Worker

## Execution

### Dependencies

Following dependencies should be setup before running project:

1. Postgresql with database - orbsight_data
2. SQS url accessible from local with aws credentials
3. Twitter credentials

Local application can be executed in two ways:

1. Run uvicorn from CLI

```shell
cd <path-to-project>/processing/observer-worker
uvicorn observer.presentation.observer_job_controller:app --reload
```

2. By executing `processing/observer-worker/observer/presentation/observer_job_controller.py` directly from your
   favourite IDE.

## Environment Variables

| Environment Variable       | Default Value  | Description                             |
|:---------------------------|:---------------|:----------------------------------------|
| **AWS_REGION**             | eu-west-1      | aws region                              |
| **AWS_ACCESS_KEY_ID**      |                | aws access key id                       |
| **AWS_SECRET_ACCESS_KEY**  |                | aws secret access key                   |
| **AWS_SQS_ANALYSER_QUEUE** |                | sqs analyser queue url                  |
| **DB_HOST**                | localhost:5432 | host and port                           |
| **CORE_DB_NAME**                | orbsight_data  | database name                           |
| **CORE_DB_USER**                | orbsight       | user username                           |
| **CORE_DB_PASSWORD**            | orbsight       | user password                           |
| twitter_consumer_key       |                | Twitter consumer key                    |
| twitter_consumer_secret    |                | Twitter consumer secret                 |
| twitter_bearer_token       |                | Twitter bearer token for authentication |

## Flows

For SQS event payload sample check json files in directory - `processing/analyzer-worker/api_call/event_ingestion`

### Twitter

Command to hit API

```shell
bash -x processing/observer-worker/api_call/job_ingestion/curl_call.sh twitter_job.json
```

### Android

Command to hit API

```shell
bash -x processing/observer-worker/api_call/job_ingestion/curl_call.sh android_job.json
```

### iOS

Command to hit API

```shell
bash -x processing/observer-worker/api_call/job_ingestion/curl_call.sh ios_job.json
```
