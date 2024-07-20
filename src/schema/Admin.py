from pydantic import BaseModel, EmailStr

class AdminBase(BaseModel):
    email: EmailStr

class AdminCreate(AdminBase):
    password: str

class AdminInDB(AdminBase):
    id: int
    hashed_password: str

    class Config:
        orm_mode = True