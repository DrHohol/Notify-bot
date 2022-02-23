import os

from dotenv import load_dotenv
from sqlalchemy import (BigInteger, Boolean, Column, DateTime, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

load_dotenv()

engine = create_engine(os.environ.get("DATABASE_URL"))

Base = declarative_base()


class Notifies(Base):
    __tablename__ = "notifies"
    id = Column(Integer, primary_key=True)
    message_text = Column(String)
    reply_id = Column(Integer)
    time = Column(DateTime)
    repeats = Column(Integer)
    chat_id = Column(BigInteger)

    def __repr__(self):

        return f"Notify {self.message_text} will be repeated {self.repeats} times"


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
