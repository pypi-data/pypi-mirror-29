import argparse
import logging
import os.path

import sqs_event.setup as setup
from sqs_event.dispatcher import dispatch, HANDLERS
from sqs_event.normalize import normalize
import sqs_event.queue as queue
import sqs_event.user as user


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def init(config):
    queue.setup(config)
    user.setup(config)


def run():
    while True:
        try:
            message = queue.recv()
            try:
                event = normalize(message.body)
                dispatch(event)
            except Exception:
                log.exception('unable to handle message={}'.format(message.id))
            else:
                queue.delete(message)
        except KeyboardInterrupt:
            log.info('Received shutdown command from keyboard')
            break
        except Exception:
            log.exception('exception encountered')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        '--config', default='config',
        help='name of the config file',
    )
    parser.add_argument(
        '-c', '--config_only', default=False, action='store_true',
        help='display config values and stop',
    )
    parser.add_argument(
        '--event', default='event',
        help='name of the event definition file',
    )
    parser.add_argument(
        '--events_only', default=False, action='store_true',
        help='display event handlers and stop',
    )
    args = parser.parse_args()

    setup.load(args.event)
    if os.path.exists(args.config):
        try:
            setup.CONFIG._load(args.config)
        except Exception as e:
            raise Exception(e)
    if args.config_only:
        print(setup.CONFIG)
    elif args.events_only:
        print(HANDLERS)
    else:
        init(setup.CONFIG)
        log.info('listening on queue: {}'.format(queue.QUEUE.url))
        run()
