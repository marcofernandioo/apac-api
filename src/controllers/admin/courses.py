from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from typing_extensions import Annotated
from typing import List

from src.schema.Course import CourseRead, CourseCreate, CourseBase, CourseUpdate
from src.models.Course import Course
from src.connector import get_db
from src.auth.decorators import admin_required
from src.auth.jwt import get_current_user, RoleChecker

router = APIRouter()

# Create Course
@router.post('/course', response_model = CourseCreate, dependencies = [Depends(RoleChecker(["admin"]))])
def create_course(course: CourseCreate, db: Annotated[Session, Depends(get_db)], current_user: dict = Depends(get_current_user)):
    db_course = Course(coursename=course.coursename)
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

# Create Course
@router.get('/course/all', response_model = List[CourseRead], dependencies = [Depends(RoleChecker(["admin"]))])
def create_course(db: Annotated[Session, Depends(get_db)], current_user: dict = Depends(get_current_user)):
    all_courses = db.query(Course).all()
    return all_courses;

# Delete Course with certain ID.
@router.delete('/course/{course_id}', response_model=None, dependencies = [Depends(RoleChecker(["admin"]))])
def delete_course(course_id: int, db: Annotated[Session, Depends(get_db)], current_user: dict = Depends(get_current_user)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db.delete(db_course)
    db.commit()
    return {"message": f"Course {course_id} has been deleted successfully"}

# Update Course
@router.put('/course/{course_id}', response_model=CourseCreate, dependencies = [Depends(RoleChecker(["admin"]))])
def update_course(course_id: int, course: CourseUpdate, db: Annotated[Session, Depends(get_db)], current_user: dict = Depends(get_current_user)):
    db_course = db.query(Course).filter(Course.id == course_id).first()
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    
    db_course.coursename = course.coursename
    db.commit()
    db.refresh(db_course)
    return db_course
