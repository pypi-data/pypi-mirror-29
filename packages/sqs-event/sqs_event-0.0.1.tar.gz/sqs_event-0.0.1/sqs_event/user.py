import logging

from ergaleia.config import Mini
from ergaleia.import_by_path import import_by_path


log = logging.getLogger(__name__)


USER = Mini(
    'setup',
)


def add_user_setup(path):
    USER.setup = (path, import_by_path(path))


def setup(config):
    if USER.setup is not None:
        path, fn = USER.setup
        log.info('calling user setup: {}'.format(path))
        fn(config)
