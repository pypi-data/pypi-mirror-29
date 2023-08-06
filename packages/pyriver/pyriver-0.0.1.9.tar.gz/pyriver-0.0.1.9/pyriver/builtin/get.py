import requests

from pyriver.services import stream_service
from pyriver.services import event_service


def execute(args):
    """ Retrieve data from another stream """
    # TODO: This needs to be implemented correctly using the routing
    parts = args.stream.split("/")
    user = None
    name = parts[0]
    if len(parts) > 1:
        user = args.stream.split("/")[0]
        name = args.stream.split("/")[1]
    stream = stream_service.get_by_name(name, user)
    events = event_service.get_events(stream, 0, args.start_date, args.end_date)
    for event in events:
        print (event_service.to_doc(event))
