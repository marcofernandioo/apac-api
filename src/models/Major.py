from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.connector import Base

class Major(Base):
    __tablename__ = "majors"
    
    id = Column(Integer, primary_key = True, index = True)
    majorname = Column(String(200), index = True)
    programme_id = Column(Integer, ForeignKey("programmes.id"))