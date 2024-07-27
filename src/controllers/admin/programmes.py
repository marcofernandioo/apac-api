from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from typing_extensions import Annotated
from typing import List

from src.schema.Programme import ProgrammeRead, ProgrammeCreate, ProgrammeBase, ProgrammeUpdate
from src.models.Programme import Programme
from src.connector import get_db
from src.auth.jwt import get_current_user, RoleChecker

router = APIRouter()

# Create
@router.post("/programmes/", response_model= ProgrammeRead, dependencies = [Depends(RoleChecker(["admin"]))])
def create_programme(programme: ProgrammeCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_programme = Programme(**programme.dict())
    db.add(db_programme)
    db.commit()
    db.refresh(db_programme)
    return db_programme

# Read (all)
@router.get("/programmes/", response_model=List[ProgrammeRead], dependencies = [Depends(RoleChecker(["admin"]))])
def read_programmes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    programmes = db.query(Programme).offset(skip).limit(limit).all()
    return programmes

# Read (single)
@router.get("/programmes/{programme_id}", response_model= ProgrammeRead, dependencies = [Depends(RoleChecker(["admin"]))])
def read_programme(programme_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_programme = db.query(Programme).filter(Programme.id == programme_id).first()
    if db_programme is None:
        raise HTTPException(status_code=404, detail="Programme not found")
    return db_programme

# Update
@router.patch("/programmes/{programme_id}", response_model= ProgrammeRead)
def update_programme(programme_id: int, programme: ProgrammeUpdate, db: Session = Depends(get_db)):
    db_programme = db.query(Programme).filter(Programme.id == programme_id).first()
    if db_programme is None:
        raise HTTPException(status_code=404, detail="Programme not found")
    
    for key, value in programme.dict(exclude_unset=True).items():
        setattr(db_programme, key, value)
    
    db.commit()
    db.refresh(db_programme)
    return db_programme

# Delete
@router.delete("/programmes/{programme_id}", response_model= ProgrammeRead, dependencies = [Depends(RoleChecker(["admin"]))])
def delete_programme(programme_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_programme = db.query(Programme).filter(Programme.id == programme_id).first()
    if db_programme is None:
        raise HTTPException(status_code=404, detail="Programme not found")
    
    db.delete(db_programme)
    db.commit()
    return db_programme
