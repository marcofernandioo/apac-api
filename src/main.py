from fastapi import FastAPI, HTTPException, Depends, status
from typing import List
from pydantic import BaseModel
from typing_extensions import Annotated # Import from here instead of pydantic.

from src.connector import engine, SessionLocal, Base

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from src.schema.Group import GroupRead, GroupCreate, GroupBase
from src.schema.Intake import IntakeRead, IntakeCreate, IntakeBase
from src.schema.Semester import SemesterRead, SemesterCreate, SemesterBase, SemesterListInput, SemesterUpdate
from src.schema.Course import CourseRead, CourseCreate, CourseBase, CourseUpdate
from src.schema.Major import MajorBase, MajorCreate, MajorRead, MajorUpdate
from src.schema.Programme import ProgrammeBase, ProgrammeCreate, ProgrammeRead, ProgrammeUpdate

from src.models.Record import Record
from src.models.Group import Group
from src.models.Intake import Intake
from src.models.Semester import Semester
# from src.models.Course import Course
# from src.models.Programme import Programme
# from src.models.Major import Major
 
from src.controllers.admin import courses, programmes, majors
from src.controllers.scheduler import semesters, intakes
from src.auth import routes

from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(courses.router, prefix="/admin/courses", tags=["admin", "courses"])
app.include_router(programmes.router, prefix="/admin/programmes", tags=["admin", "programmes"])
app.include_router(majors.router, prefix="/admin/majors", tags=["admin", "major"])

app.include_router(semesters.router, prefix="/admin/intakes", tags=["scheduler", "intakes"])
app.include_router(intakes.router, prefix="/admin/semesters", tags=["scheduler", "semesters"])

app.include_router(routes.router, prefix="/auth", tags=["auth"])

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.get("/")
def root():
    return {"data": "dllm pghkc!"};

@app.get("/xh")
def lllm():
    return {"meh": "data"}

records_list: List[Record] = []

@app.post("/records", status_code=201, response_model=Record)
def create_record(record: Record):
    print(record)
    records_list.append(record)
    return record

@app.get("/records/all")
def get_all_records():
    return {"data": "no records for now!", "status": "", "loumou": "lei's"}

@app.get('/testpost/get')
def testpost_get(db: db_dependency):
    user = db.query(TestPost).first()
    return user

# Create a Group
@app.post('/group', response_model=GroupRead)
def create_group(group: GroupCreate, db: Annotated[Session, Depends(get_db)]):
    db_group = Group(groupname=group.groupname) 
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

# Get all groups
@app.get('/group/all', response_model=List[GroupRead])
def get_all_groups(db: Annotated[Session, Depends(get_db)]):
    groups = db.query(Group).all()
    return groups


if __name__ == "__main__":
    print("connected to db.")