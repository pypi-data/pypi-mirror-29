import json


class Event(object):

    def __init__(self, _name, *args, **kwargs):
        self.name = _name
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return 'Event={} args={}, kwargs{}'.format(
            self.name, self.args, self.kwargs
        )

    @property
    def json(self):
        return json.dumps(dict(
            name=self.name,
            args=self.args,
            kwargs=self.kwargs,
        ))
