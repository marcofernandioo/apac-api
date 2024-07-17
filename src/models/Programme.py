from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
# from .database import Base
from src.connector import Base

class Programme(Base):
    __tablename__ = "programmes"

    id = Column(Integer, primary_key=True, index=True)
    programmename = Column(String(50), index=True)
    semesters = Column(Integer)
    course_id = Column(Integer, ForeignKey("course.id"))

    # course = relationship("Course", back_populates="majors")