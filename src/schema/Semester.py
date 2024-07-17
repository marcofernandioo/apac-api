# from pydantic import BaseModel
# from pydantic.types import date
# from typing import Optional, List

# class SemesterBase(BaseModel):
#     name: str
#     startdate: date
#     enddate: date
#     duration: int
#     midsemstart: date
#     midsemend: date
#     midsemduration: int
#     bufferstart: date
#     bufferend: date
#     buffersemduration: int
#     examstart: date
#     examend: date
#     examduration: int
#     intakeid: int

# class SemesterCreate(SemesterBase):
#     pass

# class SemesterRead(SemesterBase):
#     name: Optional[str] = None
#     startdate: Optional[date] = None
#     enddate: Optional[date] = None
#     duration: Optional[int] = None
#     midsemstart: Optional[date] = None
#     midsemend: Optional[date] = None
#     midsemduration: Optional[int] = None
#     bufferstart: Optional[date] = None
#     bufferend: Optional[date] = None
#     buffersemduration: Optional[int] = None
#     examstart: Optional[date] = None
#     examend: Optional[date] = None
#     examduration: Optional[int] = None
#     intakeid: Optional[int] = None

#     class Config:
#         orm_mode = True
        
# class SemesterListInput(BaseModel):
#     semesters: List[SemesterBase]


from pydantic import BaseModel
from pydantic.types import date
from typing import Optional, List

class SemesterBase(BaseModel):
    name: str
    startdate: date
    enddate: date
    midsemstart: date
    midsemend: date
    midsemduration: int
    bufferstart: date
    bufferend: date
    buffersemduration: int
    examstart: date
    examend: date
    examduration: int
    intakeid: int

class SemesterCreate(SemesterBase):
    pass

class SemesterRead(SemesterBase):
    id: int

    class Config:
        orm_mode = True

class SemesterUpdate(BaseModel):
    name: Optional[str] = None
    startdate: Optional[date] = None
    enddate: Optional[date] = None
    duration: Optional[int] = None
    midsemstart: Optional[date] = None
    midsemend: Optional[date] = None
    midsemduration: Optional[int] = None
    bufferstart: Optional[date] = None
    bufferend: Optional[date] = None
    buffersemduration: Optional[int] = None
    examstart: Optional[date] = None
    examend: Optional[date] = None
    examduration: Optional[int] = None
    intakeid: Optional[int] = None

class SemesterListInput(BaseModel):
    semesters: List[SemesterBase]