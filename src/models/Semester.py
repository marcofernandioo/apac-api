from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from src.connector import Base

class Semester(Base):
    __tablename__ = 'semester'
    
    id = Column(Integer, primary_key = True, index = True)
    name = Column(String(50))
    startdate = Column(Date)
    enddate = Column(Date) 
    duration = Column(Integer)
    midsemstart = Column(Date)
    midsemend = Column(Date)
    midsemduration = Column(Integer)
    bufferstart = Column(Date)
    bufferend = Column(Date)
    buffersemduration = Column(Integer)
    examstart = Column(Date)
    examend = Column(Date)
    examduration = Column(Integer)
    intakeid = Column(Integer, ForeignKey('intake.id'))