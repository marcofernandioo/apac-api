from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from typing_extensions import Annotated
from typing import List

from src.connector import get_db
from src.schema.Intake import IntakeRead, IntakeCreate, IntakeBase
from src.models.Intake import Intake

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
def get_all_intake(db: Annotated[Session, Depends(get_db)]):
    intake = db.query(Intake).all()
    return intake
