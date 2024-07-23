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
    coursename: str

class CourseRead(CourseBase):
    id: int
    
    class Config:
        orm_mode = True