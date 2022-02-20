from sqlalchemy import (Boolean, Column, DateTime, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("postgresql+psycopg2:///notifier_db")

Session = sessionmaker(engine)
session = Session()
Base = declarative_base()


class Notifies(Base):
    __tablename__ = 'notifies'
    id = Column(Integer, primary_key=True)
    message_text = Column(String)
    reply_id = Column(Integer)
    time = Column(DateTime)
    repeats = Column(Integer)

    def __repr__(self):

        return f'Notify {self.message_text} will be repeated {self.repeats} times'
#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)