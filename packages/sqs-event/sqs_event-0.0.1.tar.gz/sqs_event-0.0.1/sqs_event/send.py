import argparse

import boto3

from sqs_event.event import Event
from ergaleia.to_args import to_args


parser = argparse.ArgumentParser(
    description='Add an event to an SQS queue',
)
parser.add_argument('queue_name')
parser.add_argument('event_name')
parser.add_argument('arguments', nargs='*', help='args & kwargs for event')
cmdl = parser.parse_args()

args, kwargs = to_args(' '.join(cmdl.arguments))

event = Event(cmdl.event_name, *args, **kwargs)

sqs = boto3.client('sqs')
url = sqs.get_queue_url(QueueName=cmdl.queue_name)['QueueUrl']
response = sqs.send_message(
    QueueUrl=url,
    MessageBody=event.json,
)
print(response['MessageId'])
