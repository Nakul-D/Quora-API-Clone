from .database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP


class User(Base):
    __tablename__ = 'users'

    userId = Column(Integer, nullable=False, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    username = Column(String, nullable=False)
    bio = Column(String)
    createTime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    lastUpdated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Question(Base):
    __tablename__ = 'questions'

    questionId = Column(Integer, nullable=False, primary_key=True)
    question = Column(String, nullable=False)
    userId = Column(Integer, ForeignKey('users.userId', ondelete='CASCADE'), nullable=False)
    createTime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    lastUpdated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    edited = Column(Boolean, nullable=False, server_default='False')

class Answer(Base):
    __tablename__ = 'answers'

    answerId = Column(Integer, nullable=False, primary_key=True)
    questionId = Column(Integer, ForeignKey('questions.questionId', ondelete='CASCADE'), nullable=False)
    answer = Column(String, nullable=False)
    userId = Column(Integer, ForeignKey('users.userId', ondelete='CASCADE'), nullable=False)
    createTime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    lastUpdated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    edited = Column(Boolean, nullable=False, server_default='False')

class Votes(Base):
    __tablename__ = 'votes'

    answerId = Column(Integer, ForeignKey('answers.answerId', ondelete='CASCADE'), nullable=False, primary_key=True)
    userId = Column(Integer, ForeignKey('users.userId', ondelete='CASCADE'), nullable=False, primary_key=True)
    vote = Column(Boolean, nullable=False)
    createTime = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    lastUpdated = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    edited = Column(Boolean, nullable=False, server_default='False')
