from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from typing_extensions import Annotated
from typing import List

from src.connector import get_db
from src.schema.Major import MajorRead, MajorCreate, MajorBase, MajorUpdate
from src.models.Major import Major

router = APIRouter()

# Create Major
@router.post('/major', response_model = MajorRead)
def create_major(major: MajorCreate, db: Session = Depends(get_db)):
    db_major = Major(**major.dict())
    db.add(db_major) 
    db.commit()
    db.refresh(db_major)
    return db_major


# Read one Major
@router.get('/major/{major_id}', response_model = MajorRead)
def read_major(major_id: int, db: Session = Depends(get_db)):
    db_major = db.query(Major).filter(Major.id == major_id).first()
    if db_major is None:
        raise HTTPException(status_code=404, detail="Major not found")
    return db_major

# Read all Majors
@router.get("/majors/", response_model=List[MajorRead])
def read_majors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    majors = db.query(Major).offset(skip).limit(limit).all()
    return majors

# Update One Major
@router.put("/majors/{major_id}", response_model=MajorRead)
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
@router.delete("/majors/{major_id}", response_model=MajorRead)
def delete_major(major_id: int, db: Session = Depends(get_db)):
    db_major = db.query(Major).filter(Major.id == major_id).first()
    if db_major is None:
        raise HTTPException(status_code=404, detail="Major not found")
    db.delete(db_major)
    db.commit()
    return db_major
