from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from pyriver.models.base import BaseModel


class Channel(BaseModel):
    __tablename__ = "channel"
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_date = Column(Text, default=datetime.utcnow().isoformat)
    modify_date = Column(Text, default=datetime.utcnow().isoformat)
    name = Column(Text)
    stream_id = Column(Text, ForeignKey("stream.id"))
    stream = relationship("Stream", uselist=False, back_populates="ochannel")
    subscribers = relationship(
        "Stream",
        lazy="dynamic",
        secondary="stream_channel_join",
        back_populates="ichannels"
    )

    @classmethod
    def get_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
