# Observer Worker

## Execution

### Dependencies

Following dependencies should be setup before running project:
1. Postgresql with database - obsights_rbi
2. SQS url accessible from local with aws credentials
3. Twitter credentials

Local application can be executed in two ways:
1. Run uvicorn from CLI
```shell
cd <path-to-project>/processing/observer-worker
uvicorn observer.presentation.observer_job_controller:app --reload
```
2. By executing `processing/observer-worker/observer/presentation/observer_job_controller.py` directly from your favourite IDE.

## Environment Variables

| Environment Variable       | Default Value  | Description                             |
|:---------------------------|:---------------|:----------------------------------------|
| **AWS_REGION**             | eu-west-1      | aws region                              |
| **AWS_ACCESS_KEY_ID**      |                | aws access key id                       |
| **AWS_SECRET_ACCESS_KEY**  |                | aws secret access key                   |
| **AWS_SQS_ANALYSER_QUEUE** |                | sqs analyser queue url                  |
| **DB_HOST**                | localhost:5432 | host and port                           |
| **DB_NAME**                | obsights_rbi   | database name                           |
| **DB_USER**                | obsights       | user username                           |
| **DB_PASSWORD**            | obsights       | user password                           |
| twitter_consumer_key       |                | Twitter consumer key                    |
| twitter_consumer_secret    |                | Twitter consumer secret                 |
| twitter_bearer_token       |                | Twitter bearer token for authentication |

## Flows

### Twitter

Command to hit API
```shell
bash -x processing/observer-worker/api_call/job_ingestion/curl_call.sh twitter_job.json
```

SQS event payload
```json
{
    "company_id": 1,
    "entity": {
        "city": null,
        "country": null,
        "identifier": 1435,
        "simple_name": "SBM BANK (INDIA) LTD.",
        "type": "bank"
    },
    "observer": {
        "identifier": 1137,
        "name": "sbmbankindia",
        "type": "twitter"
    },
    "text_data": {
        "identifier": 365,
        "raw_text": "@wuweiquest @cifhans311 @none @KutoaCapital @lollafrens @xelaearth @BelfortNFT @Bryanvee.eth @sly_doubt @marmijo @0xbeignet"
    }
}
```

### Android 

Command to hit API
```shell
bash -x processing/observer-worker/api_call/job_ingestion/curl_call.sh android_job.json
```

SQS event payload
```json
{
    "company_id": 1,
    "entity": {
        "city": null,
        "country": null,
        "identifier": 1403,
        "simple_name": "Bank of India",
        "type": "bank"
    },
    "observer": {
        "identifier": 953,
        "name": "BOI Mobile",
        "type": "android"
    },
    "text_data": {
        "identifier": 357,
        "raw_text": "Very good app"
    }
}
```

### iOS

Command to hit API
```shell
bash -x processing/observer-worker/api_call/job_ingestion/curl_call.sh ios_job.json
```

SQS event payload
```json
{
    "company_id": 1,
    "entity": {
        "city": "Londo",
        "country": "UK",
        "identifier": 1330,
        "simple_name": "Fast Encash Money Transfer Services",
        "type": "Cross border Money Transfer in-bound only"
    },
    "observer": {
        "identifier": 819,
        "name": "Skrill - Pay & Transfer Money",
        "type": "ios"
    },
    "text_data": {
        "identifier": 364,
        "raw_text": "Deposits. I don't understand why it takes so long after clearing my bank to receive a bank wire transfer? I made 3 deposits within 24 hours and that was on the 22nd going into the 23rd I finally received access to one of those deposits earlier today the 26th and going into the 27th now I still have yet to receive the other two deposits. When I tried contacting them via messaging, I didn't get a response the ticket was just marked as resolved until I addressed that as well and then I was still told after 5 days then reach back out to them. That is ridiculous.."
    }
}
```
