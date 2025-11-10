from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from datetime import datetime

Base = declarative_base()

# Tabela associativa para muitos-para-muitos entre Session e Tag
session_tags = Table(
    'session_tags',
    Base.metadata,
    Column('session_id', ForeignKey('sessions.id'), primary_key=True),
    Column('tag_id', ForeignKey('tags.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    sessions = relationship('Session', back_populates='user')

class Session(Base):
    __tablename__ = 'sessions'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='sessions')
    emotions = relationship('Emotion', back_populates='session')
    tags = relationship('Tag', secondary=session_tags, back_populates='sessions')

class Emotion(Base):
    __tablename__ = 'emotions'
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sessions.id'))
    label = Column(String)  # Ex: alegria, medo, raiva
    intensity = Column(Integer)  # Escala de 0 a 100

    session = relationship('Session', back_populates='emotions')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)

    sessions = relationship('Session', secondary=session_tags, back_populates='tags')
