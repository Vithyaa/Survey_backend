from sqlalchemy import create_engine, Column, Integer, String, Text, Time, ForeignKey, TIMESTAMP
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    answer = Column(Text)
    time = Column(Time)
    language_id = Column(Integer, ForeignKey('language.id'))
    deleted = Column(Integer)
    record_status = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    questioned_id = Column(Integer)
    response_one_id = Column(Integer)
    response_two_id = Column(Integer)
    english_text = Column(String)
    japanese_text = Column(String)
    deleted = Column(Integer)
    record_status = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    deleted = Column(Integer)
    record_status = Column(Integer)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)


