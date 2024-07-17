from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from src.connector import Base

class Intake(Base):
    __tablename__ = 'intake'
    
    id = Column(Integer, primary_key = True, index = True)
    orientation = Column(Date, nullable=False)
    startdate = Column(Date, nullable=False)
    enddate = Column(Date, nullable=False)
    duration = Column(Integer, nullable=False)
    code = Column(String(50))
    groupid = Column(Integer, ForeignKey('group.id'), nullable=False) 

    
    def __repr__(self):
        return f"<Intake(id={self.id}, code={self.code}, startdate={self.startdate})>"