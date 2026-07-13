from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__="Users"
    id = Column(Integer, primary_key=True, index= True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Note(Base):
    __tablename__="Notes"
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, index=True)  # Foreign key to User table (assuming user_id is an integer)
