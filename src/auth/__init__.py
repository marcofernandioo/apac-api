from fastapi import APIRouter
# from .config import Settings
from .routes import router as auth_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
