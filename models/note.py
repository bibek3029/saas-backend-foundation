from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Note(Base):
    __tablename__="Notes"
    id = Column(Integer, primary_key=True, index= True)
    title = Column(String)
    content = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("Users.id"))  # Foreign key to User table (assuming user_id is an integer)
    owner = relationship("User", back_populates="notes")  # Relationship to User model