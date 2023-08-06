from time import time
import json

import redis

from pyriver.engine.processor import StreamProcessor
from pyriver.services import stream_service
from pyriver.services import event_service


class EventManager(object):

    def __init__(self):
        self.processors = []
        self.publisher = redis.Redis()
        self.aggregator = {}

    def init(self, schema):
        self.stream = stream_service.create(schema)
        self.schema = schema
        self.initialized = True

    def run(self):
        raise NotImplementedError()

    def handle(self, channel=None, input=None):
        timestamp = int(time())
        if input:
            timestamp = input["metadata"]["timestamp"]
        self.before_processing()
        ievent = self.stage_input(channel, input)
        result = self.process(ievent)
        oevent = self.structure_output(timestamp, result)
        self.save_event(oevent)
        self.publish(oevent)
        self.after_processing()

    def process(self, ievent=None):
        res = ievent or {}
        for processor in self.processors:
            res = processor.process(**res)
        return res

    def publish(self, oevent):
        self.publisher.publish(self.stream.ochannel, json.dumps(oevent))

    def before_processing(self, *args, **kwargs):
        pass

    def after_processing(self, *args, **kwargs):
        pass

    def stage_input(self, channel=None, ievent=None):
        pass

    def save_event(self, event):
        event_service.create_event(self.stream, event)

    def processor(self, index):
        def decorator(f):
            proc = StreamProcessor(f)
            self.processors.insert(index-1, proc)
            return f
        return decorator

    def structure_output(self, timestamp, result):
        res = {}
        meta = {}
        meta['timestamp'] = timestamp
        meta['stream'] = self.stream.name
        res['metadata'] = meta
        res['data'] = result
        return res
