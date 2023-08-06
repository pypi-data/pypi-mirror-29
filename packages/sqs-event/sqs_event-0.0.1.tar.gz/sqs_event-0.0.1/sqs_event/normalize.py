from sqs_event.event import Event


def normalize(data):

    # command/kwargs style
    try:
        command = data['command']
        return Event(command, **data['data'])
    except Exception:
        pass

    # name/args/kwargs style
    try:
        name = data['name']
        return Event(name, *data['args'], **data['kwargs'])
    except Exception:
        pass

    # AWS S3
    try:
        aws = data['Records'][0]
        name = aws['eventSource']
        if name != 'aws:s3':
            raise Exception('unhandled AWS event type: {}'.format(name))
        s3 = aws['s3']
        return Event(
            'S3',
            bucket=s3['bucket']['name'],
            key=s3['object']['key'],
        )
    except Exception:
        pass

    raise Exception('unable to normalize message data')
