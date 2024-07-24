from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
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
from src.schema.Parent import AssignableResponse

from src.models.Record import Record
from src.models.Group import Group
from src.models.Intake import Intake
from src.models.Semester import Semester
from src.models.Course import Course
from src.models.Programme import Programme
# from src.models.Major import Major
 
from src.controllers.admin import courses, programmes, majors
from src.controllers.scheduler import semesters, intakes
from src.auth import routes

from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True, 
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses.router, prefix="/admin", tags=["admin", "courses"])
app.include_router(programmes.router, prefix="/admin", tags=["admin", "programmes"])
app.include_router(majors.router, prefix="/admin", tags=["admin", "major"])

app.include_router(semesters.router, prefix="/scheduler", tags=["scheduler", "semesters"])
app.include_router(intakes.router, prefix="/scheduler", tags=["scheduler", "intakes"])

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
    db_group = Group(**group.dict())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

# Get all groups
@app.get('/group/all', response_model=List[GroupRead])
def get_all_groups(
    db: Annotated[Session, Depends(get_db)],
    parentid: Optional[int] = Query(None, description="Parent ID to filter groups"),
    parenttype: Optional[str] = Query(None, description="Parent type to filter groups")
):
    groups = db.query(Group)
    if parenttype is not None: 
        querytype = groups.filter(Group.parenttype == parenttype)
    if parentid is not None:
        queryid = groups.filter(Group.parentid == parentid);
    groups.all()
    return groups

@app.get('/parent/all', response_model=AssignableResponse)
def get_all_parents(db: Annotated[Session, Depends(get_db)]):
    # Query for assignable courses
    assignable_courses = db.query(Course).filter(Course.assignableIntake == True).all()
    
    # Query for assignable programmes
    assignable_programmes = db.query(Programme).filter(Programme.assignableIntake == True).all()
    
    # Combine and format the results
    result = []
    for course in assignable_courses:
        result.append(CourseRead(
            id=course.id,
            coursename=course.coursename,
            assignableIntake=course.assignableIntake,
            code=course.code
        ))
    for programme in assignable_programmes:
        result.append(ProgrammeRead(
            id=programme.id,
            programmename=programme.programmename,
            semesters=programme.semesters,
            course_id=programme.course_id,
            assignableIntake=programme.assignableIntake,
            code=programme.code
        ))
   
    return AssignableResponse(items=result)

if __name__ == "__main__":
    print("connected to db.") 