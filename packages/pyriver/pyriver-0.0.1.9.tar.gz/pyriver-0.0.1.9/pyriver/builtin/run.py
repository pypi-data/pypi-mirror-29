import imp
import json

from pyriver.engine.stream import Stream


def execute(*args, **kwargs):
    with open("river.json", "rb") as riverfile:
        schema = json.load(riverfile)
        entry = schema.get("metadata", {}).get("entry")
        stream = Stream()
        if entry:
            stream = imp.load_source("stream", entry).river
        stream.init(schema)
        stream.run()
