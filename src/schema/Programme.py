from pydantic import BaseModel
from typing import Optional

class ProgrammeBase(BaseModel):
    programmename: str
    semesters: int 
    course_id: int
    assignableIntake: bool = False
    code: str

class ProgrammeCreate(ProgrammeBase):
    pass

class ProgrammeRead(ProgrammeBase):
    id: int

    class Config:
        orm_mode = True

class ProgrammeUpdate(BaseModel):
    programmename: Optional[str]
    semesters: Optional[int]
    course_id: Optional[int]
    assignableIntake: Optional[bool]
    code: Optional[str]