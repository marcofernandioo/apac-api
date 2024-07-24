from fastapi import APIRouter
from .intakes import router as intakes_router
from .semesters import router as semesters_router

router = APIRouter()

router.include_router(semesters_router, tags=["semesters"])
router.include_router(intakes_router, tags=["intakes"])

# You can also add any admin-wide dependencies or middleware here
# For example:
# from app.auth.jwt import admin_required
# router.dependencies.append(Depends(admin_required))