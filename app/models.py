from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, text, Time
from sqlalchemy.dialects.mysql import TINYINT
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String)
    name = Column(String)
    age = Column(Integer)
    answer = Column(Text)
    time = Column(Time)
    language_id = Column(Integer, ForeignKey('language.id'))
    created_at = Column(DateTime, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    record_status = Column(TINYINT(1), nullable=False,
                           server_default=text("'1'"))

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    questioned_id = Column(Integer)
    response_one_id = Column(Integer)
    response_two_id = Column(Integer)
    english_text = Column(String)
    japanese_text = Column(String)
    created_at = Column(DateTime, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    record_status = Column(TINYINT(1), nullable=False,
                           server_default=text("'1'"))

class Language(Base):
    __tablename__ = 'language'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    created_at = Column(DateTime, nullable=False,
                        server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(DateTime, server_default=text(
        "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    record_status = Column(TINYINT(1), nullable=False,
                           server_default=text("'1'"))


