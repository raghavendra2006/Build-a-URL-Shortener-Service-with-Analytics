# models.py
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Setup SQLite Database
DATABASE_URL = "sqlite:///./shortener.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UrlMapping(Base):
    __tablename__ = "url_mappings"
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to track clicks
    clicks = relationship("Click", back_populates="url_mapping")

class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True, index=True)
    url_mapping_id = Column(Integer, ForeignKey("url_mappings.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    client_ip = Column(String)
    user_agent = Column(String)

    url_mapping = relationship("UrlMapping", back_populates="clicks")

def init_db():
    Base.metadata.create_all(bind=engine)