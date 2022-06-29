from .database import Base
from sqlalchemy import Column, Integer, String
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
