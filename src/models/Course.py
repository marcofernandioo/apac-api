from sqlalchemy import Boolean, Column, Integer, String
from src.connector import Base

class Course(Base):
    __tablename__ = "course"
    
    id = Column(Integer, primary_key = True, index = True)
    coursename = Column(String(50))