from obsei.misc.utils import obj_to_json


def publish_events(sqs_consumer):
    message = {
        "tenant_id": "f9f91b0b-f976-4bd3-b956-470ffcfcf77f",
        "observer_identifier": "039d4a70-f858-48e5-9835-104cc391cfda",
        "observer_name": "BOI Mobile",
        "observer_type": 2,
        "regulated_entity_type": [
            "Bank"
        ],
        "entity_identifier": "24b483fe-6548-407c-8ef3-21b1dc45f6c4",
        "entity_simple_name": "Bank of India",
        "regulated_type": [
            "Bank"
        ],
        "lookup_period": "30d",
        "limit_count": 2,
        "url": "https://play.google.com/store/apps/details?id=com.boi.mpay"
    }
    sqs_consumer.sqs.send_message(QueueUrl=sqs_consumer.queue_url, MessageBody=obj_to_json(message).decode('UTF-8'))


def test_write_message(job_worker):
    publish_events(job_worker.consumer)
    job_worker.run_worker_process()
    assert True
