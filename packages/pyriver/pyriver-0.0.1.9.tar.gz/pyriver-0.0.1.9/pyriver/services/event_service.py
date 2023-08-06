import json

from pyriver.models import Event, joins


def create_event(stream, event):
    model = Event()
    model.timestamp = event["metadata"]["timestamp"]
    model.value = json.dumps(event)
    stream.events.append(model)
    stream.save()


def get_events(stream, page, start_date, end_date):
    return Event.query. \
        join(joins.stream_event_join, (joins.stream_event_join.c.event_id == Event.id)). \
        filter(joins.stream_event_join.c.stream_id == stream.id). \
        order_by(Event.timestamp.desc()). \
        limit(100). \
        offset(100*page). \
        all()


def to_doc(event):
    return json.loads(event.value)["data"]
