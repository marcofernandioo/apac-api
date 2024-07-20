from sqlalchemy import Boolean, Column, Integer, String
from src.connector import Base

class Scheduler(Base):
    __tablename__ = "schedulers"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(60))