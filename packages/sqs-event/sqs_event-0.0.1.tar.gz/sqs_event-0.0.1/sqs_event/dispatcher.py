import logging

from ergaleia.import_by_path import import_by_path

log = logging.getLogger(__name__)


HANDLERS = dict()


def add_event_handler(name, path):
    HANDLERS[name] = (path, import_by_path(path))


def dispatch(event):
    try:
        path, fn = HANDLERS[event.name]
    except KeyError:
        log.error("handler for event '{}' not defined".format(event.name))
        raise
    else:
        log.info("dispatching event '{}' to {}".format(event.name, path))
        fn(*event.args, **event.kwargs)
