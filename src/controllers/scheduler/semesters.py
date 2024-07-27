from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import sessionmaker, Session
from typing_extensions import Annotated
from typing import List, Optional
import json

from src.connector import get_db
from src.schema.Semester import SemesterRead, SemesterCreate, SemesterBase, SemesterUpdate, SemesterListInput
from src.models.Semester import Semester
from src.auth.jwt import get_current_user, RoleChecker

router = APIRouter()

# Create a Semester
@router.post('/semester', response_model = SemesterRead, dependencies = [Depends(RoleChecker(["scheduler"]))])
def create_semester(semester: SemesterBase, db: Annotated[Session, Depends(get_db)], current_user: dict = Depends(get_current_user)):
    db_semester = Semester(**semester.dict())
    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)
    return db_semester

@router.get('/semester/all', response_model = List[SemesterRead])
def get_all_semester(
    db: Annotated[Session, Depends(get_db)], 
    intakeid: Optional[str] = Query(None, description='Filter semesters by intake id'),
    intake_ids: Optional[str] = Query(None, description='Filter semesters by comma-separated list of intake IDs')
):
    query = db.query(Semester)
    
    if intakeid is not None:
        query = query.filter(Semester.intakeid == intakeid)
        
    if intake_ids:
        intake_id_list = [id.strip() for id in intake_ids.split(',')]
        query = query.filter(Semester.intakeid.in_(intake_id_list))
    
    semesters = query.all()
    return semesters

@router.post('/semester/create', response_model = List[SemesterRead], dependencies = [Depends(RoleChecker(["scheduler"]))])
def create_multiple_semesters(intake_id: int, semester_input: List[SemesterCreate], db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    # 1. Validation: Check if selected intake exists.
    
    # 2. Validation: Check the number of semesters in the request
    # semester_per_course = 2 # Placeholder for now.
    # if 2 != len(semester_input):
    #     raise HTTPException(status_code=400, detail="An intake cannot have more than 6 semesters")
    
    # 3. Create the Semester object
    created_sems = []
    for semester in semester_input:
        # Create new Semester object
        new_semester = Semester(
            intakeid=intake_id,
            name=semester.name,
            startdate=semester.startdate,
            enddate=semester.enddate,
            duration=semester.duration,
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
        # created_sems.routerend(new_semester)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

    return created_sems

@router.post('/semester/update', response_model=List[SemesterRead])
async def update_semesters(request: Request, intake_id: int, semester_updates: List[SemesterUpdate], db: Session = Depends(get_db)):
    try:
        body = await request.body()
        print(f"Raw: {body}")
        db.query(Semester).filter(Semester.intakeid == int(intake_id)).delete()
        new_semesters = [
            Semester(**semester.dict(exclude_unset=True), intakeid=intake_id) 
            for semester in semester_updates
        ]
        db.add_all(new_semesters)
        db.commit()
        for semester in new_semesters:
            db.refresh(semester)
        return new_semesters
    
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    