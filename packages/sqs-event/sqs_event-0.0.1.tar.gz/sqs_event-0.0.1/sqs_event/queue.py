import boto3
import json
import logging

from ergaleia.config import Mini


log = logging.getLogger(__name__)


QUEUE = Mini(
    'url',
    'wait_time validator=int',
    'visibility_timeout validator=int',
)


SQS = boto3.client('sqs')


def setup(config):
    url = SQS.get_queue_url(QueueName=config.queue.name)['QueueUrl']
    QUEUE.set(
        url=url,
        wait_time=config.queue.wait_time,
        visibility_timeout=config.queue.visibility_timeout,
    )


def recv():
    if not QUEUE.url:
        raise Exception('queue has not been setup')
    while True:
        sqs_message = SQS.receive_message(
            QueueUrl=QUEUE.url,
            WaitTimeSeconds=QUEUE.wait_time,
            VisibilityTimeout=QUEUE.visibility_timeout,
        )
        message = Message.parse(sqs_message)
        if message is not None:
            return message


def delete(message):
    SQS.delete_message(
        QueueUrl=QUEUE.url,
        ReceiptHandle=message.handle,
    )


class Message(object):

    def __init__(self, body, id, handle):
        self.body = body
        self.id = id
        self.handle = handle

    def __repr__(self):
        return json.dumps(self.body, indent=4)

    @classmethod
    def parse(cls, data):
        if 'Messages' not in data:
            return None
        try:
            data = data['Messages'][0]
            body = json.loads(data['Body'])
            handle = data['ReceiptHandle']
            id = data['MessageId']
        except Exception:
            log.exception('unable to parse message')
            return None
        else:
            return Message(body, id, handle)
