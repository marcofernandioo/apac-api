from pydantic import BaseModel
from typing import Optional

class MajorBase(BaseModel):
    majorname: str
    programme_id: int

class MajorCreate(MajorBase):
    pass

class MajorRead(MajorBase):
    id: int

    class Config:
        orm_mode = True

class MajorUpdate(MajorBase):
    majorname: Optional[str] = None
    programme_id: Optional[int] = None