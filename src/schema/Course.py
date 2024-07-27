from typing import Optional
from pydantic import BaseModel
from datetime import date

class CourseBase(BaseModel):
    coursename: str
    assignableIntake: bool = False
    code: Optional[str] = None
    
class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    coursename: Optional[str]
    assignableIntake: Optional[bool]
    code: Optional[str]

class CourseRead(CourseBase):
    id: int
    
    class Config:
        orm_mode = True