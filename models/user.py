from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class User(Base):
    __tablename__="Users"
    id = Column(Integer, primary_key=True, index= True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    notes = relationship("Note", back_populates="owner")