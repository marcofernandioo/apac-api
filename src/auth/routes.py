from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import timedelta
from functools import wraps

from src.auth.jwt import create_access_token, verify_token
# from src.models.user import User, UserInDB
from src.auth.config import settings

from src.models.Admin import Admin
from src.models.Scheduler import Scheduler

from src.schema.Admin import AdminBase, AdminCreate, AdminInDB
from src.schema.Scheduler import SchedulerBase, SchedulerCreate, SchedulerInDB
from src.schema.User import UserLogin, UserCreate

from src.connector import get_db

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

# This is a mock database. In a real application, you'd use a proper database.
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
    }
}

# JWT helper function
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not user.verify_password(password):  # You need to implement this method
        return False
    return user

# Auth helper functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# @router.post("/login-jwt")
# async def loginWithJWT(form_data: OAuth2PasswordRequestForm = Depends()):
#     user = authenticate_user(fake_users_db, form_data.username, form_data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     access_token = create_access_token(
#         data={"sub": user.username},
#         expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
#     )
#     return {"access_token": access_token, "token_type": "bearer"}

# Register endpoint
@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username already exists in either table
    existing_user = db.query(Scheduler).filter(Scheduler.email == user.email).first()
    if not existing_user:
        existing_user = db.query(Admin).filter(Admin.email == user.email).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    hashed_password = get_password_hash(user.password)

    if user.role == "admin":
        new_user = Admin(email=user.email, hashed_password=hashed_password)
    else:
        new_user = Scheduler(email=user.email, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Check Scheduler table
    db_user = db.query(Scheduler).filter(Scheduler.email == user.email).first()
    user_type = "scheduler"

    # If not found, check Admin table
    if not db_user:
        db_user = db.query(Admin).filter(Admin.email == user.email).first()
        user_type = "admin"

    # If db_user not found, or password is not verified.
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    access_token_expires = timedelta(minutes=30)  # You can adjust this value
    access_token = create_access_token(
        data={"sub": db_user.email, "role": user_type}, expires_delta=access_token_expires
    )

    return {"message": "Login successful", "token_type": "bearer", "access_token": access_token}

# @router.post("/logout")
# async def logout(current_user: User = Depends(verify_token)):
#     # In a real application, you might want to invalidate the token here
#     return {"message": "Successfully logged out"}

# @router.get("/me")
# async def read_users_me(current_user: User = Depends(verify_token)):
#     return current_user