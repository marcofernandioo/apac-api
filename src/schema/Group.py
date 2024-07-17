from pydantic import BaseModel

class GroupBase(BaseModel):
    groupname: str

class GroupCreate(GroupBase):
    pass

class GroupRead(GroupBase):
    id: int

    class Config:
        orm_mode = True