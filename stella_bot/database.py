import datetime as dt
from typing import List
from sqlalchemy import (create_engine, Column, Integer, String, Text,
                        DateTime, ForeignKey, Table)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine('sqlite:///stella_bot.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

user_tag = Table(
    'user_tag', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True)
    username = Column(String(255))
    first_name = Column(String(255))
    last_name = Column(String(255))
    last_active = Column(DateTime, default=dt.datetime.utcnow)
    interactions = relationship('Interaction', back_populates='user')
    tags = relationship('Tag', secondary=user_tag, back_populates='users')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    users = relationship('User', secondary=user_tag, back_populates='tags')

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    article = Column(String(255))
    category = Column(String(255))
    link = Column(String(255))
    description = Column(Text)
    image = Column(String(255))

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    timestamp = Column(DateTime, default=dt.datetime.utcnow)
    user = relationship('User', back_populates='interactions')


def init_db():
    Base.metadata.create_all(engine)
