import argparse
import json

import boto3


def read_json_file(filename):
    with open(filename, 'r') as f:
        return json.load(f)


def transform_message(message):
    return {
        "tenant_id": "02ddd60c-2d58-47cc-a445-275d8e621252",
        "raw_data_id": message["identifier"],
        "raw_text": message["raw_text"]
    }


def send_to_sqs(messages, queue_url, start=0, end=None):
    sqs = boto3.client('sqs')
    for message in messages[start:end]:
        transformed_message = transform_message(message)
        print(f"Sending: {json.dumps(transformed_message)}")
        try:
            response = sqs.send_message(
                QueueUrl=queue_url,
                MessageBody=json.dumps(transformed_message)
            )
            print(f"SQS response: {response}")
        except Exception as e:
            print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(description='Send messages to SQS')
    parser.add_argument('filename', type=str, help='JSON filename containing the messages')
    parser.add_argument('--start', type=int, default=0, help='Start index for sending messages')
    parser.add_argument('--end', type=int, default=None, help='End index for sending messages')
    args = parser.parse_args()

    messages = read_json_file(args.filename)
    queue_url = 'prod-analyzer'  # Replace with your SQS queue URL

    send_to_sqs(messages, queue_url, args.start, args.end)


# python publish_to_sqs.py insight_raw_data.json
if __name__ == '__main__':
    main()
