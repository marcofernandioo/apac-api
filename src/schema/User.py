from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: str
    password: str
    role: str

class UserLogin(BaseModel):
    email: str
    password: str