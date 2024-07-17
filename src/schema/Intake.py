from pydantic import BaseModel
from datetime import date
from typing import Optional

class IntakeBase(BaseModel):
    orientation: date
    startdate: date
    enddate: date
    duration: int
    code: Optional[str] = None
    groupid: int

class IntakeCreate(IntakeBase):
    pass

class IntakeRead(IntakeBase):
    id: int

    class Config:
        orm_mode = True