from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from typing_extensions import Annotated
from typing import List

from src.connector import get_db
from src.schema.Semester import SemesterRead, SemesterCreate, SemesterBase, SemesterUpdate, SemesterListInput
from src.models.Semester import Semester

router = APIRouter()

# Create a Semester
@router.post('/semester', response_model = SemesterRead)
def create_semester(semester: SemesterBase, db: Annotated[Session, Depends(get_db)]):
    db_semester = Semester(**semester.dict())
    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)
    return db_semester

@router.get('/semester/all', response_model = List[SemesterRead])
def get_all_semester(db: Annotated[Session, Depends(get_db)]):
    semester = db.query(Semester).all()
    return semester

@router.post('/semester/create', response_model = List[SemesterRead])
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
        created_sems.routerend(new_semester)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return created_sems

@router.put('/semester/update/{semester_id}', response_model=SemesterRead)
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