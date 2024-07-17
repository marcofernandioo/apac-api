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
from src.models.Course import Course
from src.models.Programme import Programme
from src.models.Major import Major
 
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

# Create an Intake
@app.post('/intake', response_model = IntakeRead)
def create_intake(intake: IntakeBase, db: Annotated[Session, Depends(get_db)]):
    db_intake = Intake(**intake.dict())
    db.add(db_intake)
    db.commit()
    db.refresh(db_intake)
    return db_intake

# Get all intakes
@app.get('/intake/all', response_model=List[IntakeRead])
def get_all_intake(db: Annotated[Session, Depends(get_db)]):
    intake = db.query(Intake).all()
    return intake

# Create a Semester
@app.post('/semester', response_model = SemesterRead)
def create_semester(semester: SemesterBase, db: Annotated[Session, Depends(get_db)]):
    db_semester = Semester(**semester.dict())
    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)
    return db_semester

@app.get('/semester/all', response_model = List[SemesterRead])
def get_all_semester(db: Annotated[Session, Depends(get_db)]):
    semester = db.query(Semester).all()
    return semester

@app.post('/semester/create', response_model = List[SemesterRead])
def create_multiple_semesters(intake_id: int, semester_input: SemesterListInput, db: Session = Depends(get_db)):
    # 1. Validation: Check if selected intake exists.
    
    # 2. Validation: Check the number of semesters in the request
    # semester_per_course = 2 # Placeholder for now.
    # if 2 != len(semester_input):
    #     raise HTTPException(status_code=400, detail="An intake cannot have more than 6 semesters")
    
    # 3. Create the Semester object
    created_sems = []
    for semester in semester_input.semesters:
        # Create new Semester object
        new_semester = Semester(
            intakeid=intake_id,
            name=semester.name,
            startdate=semester.startdate,
            enddate=semester.enddate,
            bufferstart=semester.bufferstart,
            bufferend=semester.bufferend,
            examstart=semester.examstart,
            examend=semester.examend,
            midsemstart=semester.midsemstart,
            midsemend=semester.midsemend,
            midsemduration=semester.midsemduration,
            buffersemduration=semester.buffersemduration,
            examduration=semester.examduration,
        )

        db.add(new_semester)
        created_sems.append(new_semester)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return created_sems

@app.put('/semester/update/{semester_id}', response_model=SemesterRead)
def update_semester(semester_id: int, semester_input: SemesterUpdate, db: Session = Depends(get_db)):
    # 1. Fetch the semester
    semester = db.query(Semester).filter(Semester.id == semester_id).first()
    if not semester:
        raise HTTPException(status_code=404, detail="Semester not found")

    # 2. Update the semester object
    for key, value in semester_input.dict(exclude_unset=True).items():
        setattr(semester, key, value)

    try:
        db.commit()
        db.refresh(semester)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return semester

# Create Course
@app.post('/course', response_model = CourseCreate)
def create_course(course: CourseCreate, db: Annotated[Session, Depends(get_db)]):
    db_course = Course(coursename=course.coursename)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Create Course
@app.get('/course/all', response_model = List[CourseRead])
def create_course(db: Annotated[Session, Depends(get_db)]):
    all_courses = db.query(Course).all()
    return all_courses;

# Delete Course with certain ID.
@app.delete('/course/{course_id}', response_model=None)
def delete_course(course_id: int, db: Annotated[Session, Depends(get_db)]):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(db_course)
    db.commit()
    return {"message": f"Course {course_id} has been deleted successfully"}

# Update Course
@app.put('/course/{course_id}', response_model=CourseCreate)
def update_course(course_id: int, course: CourseUpdate, db: Annotated[Session, Depends(get_db)]):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_course.coursename = course.coursename
    db.commit()
    db.refresh(db_course)
    return db_course


# Create
@app.post("/programmes/", response_model= ProgrammeRead)
def create_programme(programme: ProgrammeCreate, db: Session = Depends(get_db)):
    db_programme = Programme(**programme.dict())
    db.add(db_programme)
    db.commit()
    db.refresh(db_programme)
    return db_programme

# Read (all)
@app.get("/programmes/", response_model=List[ProgrammeRead])
def read_programmes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    programmes = db.query(Programme).offset(skip).limit(limit).all()
    return programmes

# Read (single)
@app.get("/programmes/{programme_id}", response_model= ProgrammeRead)
def read_programme(programme_id: int, db: Session = Depends(get_db)):
    db_programme = db.query(Programme).filter(Programme.id == programme_id).first()
    if db_programme is None:
        raise HTTPException(status_code=404, detail="Programme not found")
    return db_programme

# Update
@app.put("/programmes/{programme_id}", response_model= ProgrammeRead)
def update_programme(programme_id: int, programme: ProgrammeUpdate, db: Session = Depends(get_db)):
    db_programme = db.query(Programme).filter(Programme.id == programme_id).first()
    if db_programme is None:
        raise HTTPException(status_code=404, detail="Programme not found")
    
    update_data = programme.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_programme, key, value)
    
    db.commit()
    db.refresh(db_programme)
    return db_programme

# Delete
@app.delete("/programmes/{programme_id}", response_model= ProgrammeRead)
def delete_programme(programme_id: int, db: Session = Depends(get_db)):
    db_programme = db.query(Programme).filter(Programme.id == programme_id).first()
    if db_programme is None:
        raise HTTPException(status_code=404, detail="Programme not found")
    
    db.delete(db_programme)
    db.commit()
    return db_programme

# Create Major
@app.post('/major', response_model = MajorRead)
def create_major(major: MajorCreate, db: Session = Depends(get_db)):
    db_major = Major(**major.dict())
    db.add(db_major) 
    db.commit()
    db.refresh(db_major)
    return db_major


# Read one Major
@app.get('/major/{major_id}', response_model = MajorRead)
def read_major(major_id: int, db: Session = Depends(get_db)):
    db_major = db.query(Major).filter(Major.id == major_id).first()
    if db_major is None:
        raise HTTPException(status_code=404, detail="Major not found")
    return db_major

# Read all Majors
@app.get("/majors/", response_model=List[MajorRead])
def read_majors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    majors = db.query(Major).offset(skip).limit(limit).all()
    return majors

# Update One Major
@app.put("/majors/{major_id}", response_model=MajorRead)
def update_major(major_id: int, major: MajorUpdate, db: Session = Depends(get_db)):
    db_major = db.query(Major).filter(Major.id == major_id).first()
    if db_major is None:
        raise HTTPException(status_code=404, detail="Major not found")
    update_data = major.dict(exclude_unset=True)
    for key, value in update_data.items(): 
        setattr(db_major, key, value)
    db.commit()
    db.refresh(db_major)
    return db_major

# Delete One Major
@app.delete("/majors/{major_id}", response_model=MajorRead)
def delete_major(major_id: int, db: Session = Depends(get_db)):
    db_major = db.query(Major).filter(Major.id == major_id).first()
    if db_major is None:
        raise HTTPException(status_code=404, detail="Major not found")
    db.delete(db_major)
    db.commit()
    return db_major

if __name__ == "__main__":
    print("connected to db.")