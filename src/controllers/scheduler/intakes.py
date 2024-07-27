from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import extract
from sqlalchemy.orm import sessionmaker, Session, joinedload
from typing_extensions import Annotated
from typing import List, Optional

from src.connector import get_db
from src.schema.Intake import IntakeRead, IntakeCreate, IntakeBase
from src.models.Intake import Intake
from src.models.Group import Group
from src.auth.jwt import get_current_user, RoleChecker

router = APIRouter()

# Create an Intake
@router.post('/intake', response_model = IntakeRead)
def create_intake(intake: IntakeBase, db: Annotated[Session, Depends(get_db)]):
    db_intake = Intake(**intake.dict())
    db.add(db_intake)
    db.commit()
    db.refresh(db_intake)
    return db_intake

# Get all intakes
@router.get('/intake/all', response_model=List[IntakeRead])
def get_all_intake(
    db: Session = Depends(get_db),
    year: Optional[int] = Query(None, description="Filter intakes by year"),
    groupname: Optional[str] = Query(None, description="Filter intakes by group name"),
    group_ids: Optional[str] = Query(None, description="Filter intakes by comma-separated list of group IDs")
):
    query = db.query(Intake).join(Group)
    
    if year is not None:
        query = query.filter(extract('year', Intake.startdate) == year)
    
    if groupname is not None:
        query = query.filter(Group.groupname == groupname)
    
    if group_ids:
        group_id_list = [int(id) for id in group_ids.split(',')]
        query = query.filter(Intake.groupid.in_(group_id_list))
    
    intakes = query.all()
    return intakes
