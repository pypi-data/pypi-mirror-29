import json

from pyriver.db import db
from pyriver.models import Stream, Channel


def create(schema):
    if not validate_schema(schema):
        return None
    stream = Stream()
    meta = schema['metadata']
    stream.name = meta.get('name')
    stream.description = meta.get('description')
    stream.entry_point = meta.get('entry_point')
    stream.raw_schema = json.dumps(schema)
    stream.user = "ptbrodie"
    channel = Channel()
    channel.name = "%s/%s" % (stream.user, stream.name)
    stream.ochannel = channel
    stream.ichannels = []
    if schema['data']:
        for channel in get_ichannels(schema):
            stream.ichannels.append(channel)
    stream.save()
    return stream


def validate_schema(schema):
    return True


def get_ichannels(schema):
    # TODO: recursive case is to return all leaves
    channels = set()
    for k, v in schema['data'].items():
        if k == "_comment":
            continue
        channels.add(v.split('.')[0])
    res = []
    for channel in channels:
        res += Channel.get_by_name(channel)
    return res


def get_by_id(stream_id):
    return Stream.query.filter_by(id=stream_id).first()


def get_by_name(name, user):
    return Stream.query.filter_by(name=name).first()


def to_doc(stream):
    return {
        "id": stream.id,
        "name": stream.name,
        "description": stream.description,
        "links": {
            "events": "/streams/{}/events".format(stream.id),
            "info": "/streams/{}".format(stream.id)
        }
    }


def get_river_json(schemafile="river.json"):
    with open(schemafile, "rb") as riverfile:
        return json.load(riverfile)
