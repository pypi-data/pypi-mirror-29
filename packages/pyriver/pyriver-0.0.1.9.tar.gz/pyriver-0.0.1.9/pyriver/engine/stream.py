import redis

from pyriver.engine.manager import EventManager
from pyriver.engine.listener import Listener
from pyriver.services import stream_service


class Stream(EventManager):

    def __init__(self):
        self.processors = []

    def init(self, schema):
        self.stream = stream_service.create(schema)
        self.publisher = redis.Redis()

    def run(self):
        for channel in self.stream.ichannels:
            listener = Listener(channel, self)
            listener.start()

    def stage_ievent(self, channel, ievent):
        event = json.loads(ievent['data'])
        timestamp = event['metadata']['timestamp']
        channel_events = self.aggregator.get(timestamp, {})
        # TODO: possible we overwrite an event here on a larger time interval
        channel_events[channel] = event
        self.aggregator[timestamp] = channel_events
        for channel in self.stream.ichannels:
            if channel not in channel_events:
                return
        self.handle(timestamp, channel_events)

    def build_oevent(self, stream, timestamp, channel_events):
        oevent = {}
        metadata = {}
        data = {}
        metadata['timestamp'] = timestamp
        metadata['stream'] = stream.name
        for key, path in stream.ischema.iteritems():
            if key == "_comment":
                continue
            data[key] = self.get_value(path, channel_events)
        oevent['data'] = data
        oevent['metadata'] = metadata
        return oevent

    def get_value(self, path, events):
        tokens = path.split('.')
        if not tokens:
            return None
        curr = events[tokens[0]]
        for token in tokens[1:]:
            curr = curr[token]
        return curr


    def handle(self, timestamp, channel_events):
        revent = self.build_oevent(self.stream, timestamp, channel_events)
        result = self.process(revent)
        oevent = self.structure_result(timestamp, result)
        self.save_event(oevent)
        self.publish(oevent)


    def process(self, event):
        res = event
        for processor in self.processors:
            res = processor.process(**event)
        return res
