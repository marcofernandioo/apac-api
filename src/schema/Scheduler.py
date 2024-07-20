from pydantic import BaseModel, EmailStr

class SchedulerBase(BaseModel):
    email: EmailStr

class SchedulerCreate(SchedulerBase):
    password: str

class SchedulerInDB(SchedulerBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True