from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    image_path = Column(String(500))
    scheduled_time = Column(DateTime)
    status = Column(String(20), default='draft')
    post_urn = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    analytics = relationship('Analytics', back_populates='post', cascade='all, delete-orphan')

class Analytics(Base):
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id'))
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    checked_at = Column(DateTime, default=datetime.utcnow)
    
    post = relationship('Post', back_populates='analytics')

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
else:
    engine = None
    SessionLocal = None

def init_db():
    if engine:
        Base.metadata.create_all(bind=engine)
    else:
        raise Exception("DATABASE_URL not configured")

def get_db():
    if SessionLocal:
        return SessionLocal()
    raise Exception("Database not initialized")
