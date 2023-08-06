from flask import Blueprint, jsonify, request

from pyriver.services import stream_service, event_service
from pyriver.models import Stream


bp = Blueprint("api", __name__)


@bp.route("/streams")
def get_streams():
    streams = Stream.query.all()
    schemas = []
    for stream in streams:
        schemas.append(stream_service.to_doc(stream))
    return jsonify(streams=schemas)


@bp.route("/streams/<stream_id>")
def get_stream(stream_id):
    stream = stream_service.get_by_id(stream_id)
    if stream:
        return jsonify(stream=stream_service.to_doc(stream))
    return "Stream %s not found." % stream_id, 404


@bp.route("/streams/<stream_id>/events")
def get_events(stream_id):
    stream = stream_service.get_by_id(stream_id)
    if not stream:
        return "Stream %s not found." % stream_id, 404
    page = request.args.get("page", 0)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    events = event_service.get_events(stream, page, start_date, end_date)
    result = []
    for event in events:
        result.append(event_service.to_doc(event))
    return jsonify(events=result)
