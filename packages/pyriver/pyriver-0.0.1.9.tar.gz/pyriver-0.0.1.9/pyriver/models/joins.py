from sqlalchemy import Table, Column, Integer, ForeignKey

from pyriver.models.base import BaseModel
from pyriver.models import Stream, Channel    # noqa


stream_event_join = Table(
    'stream_event_join',
    BaseModel.metadata,
    Column('stream_id', Integer, ForeignKey('stream.id'), index=True),
    Column('event_id', Integer, ForeignKey('event.id'), index=True),
)

stream_channel_join = Table(
    'stream_channel_join',
    BaseModel.metadata,
    Column('stream_id', Integer, ForeignKey('stream.id'), index=True),
    Column('channel_id', Integer, ForeignKey('channel.id'), index=True),
)
