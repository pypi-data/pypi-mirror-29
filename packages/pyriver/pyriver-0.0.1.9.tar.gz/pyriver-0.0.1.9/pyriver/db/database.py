from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class DB(object):

    def __init__(self):
        self.Model = declarative_base()
        self.engine = create_engine('sqlite:///.river/river.db')
        Session = sessionmaker()
        self.session = Session(bind=self.engine)

    def initdb(self):
        self.Model.metadata.create_all(self.engine)

    def nukedb(self):
        self.Model.metadata.drop_all(self.engine)
        self.initdb()
