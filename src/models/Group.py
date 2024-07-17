from sqlalchemy import Boolean, Column, Integer, String
from src.connector import Base

class Group(Base):
    __tablename__ = 'group'
    
    id = Column(Integer, primary_key = True, index = True)
    groupname = Column(String(50))