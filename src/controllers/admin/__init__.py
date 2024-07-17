from fastapi import APIRouter
from .courses import router as courses_router
from .programmes import router as programmes_router
from .majors import router as majors_router

router = APIRouter()

router.include_router(courses_router, prefix="/courses", tags=["courses"])
print("llm")
router.include_router(programmes_router, prefix="/programmes", tags=["programmes"])
router.include_router(majors_router, prefix="/majors", tags=["majors"])

# You can also add any admin-wide dependencies or middleware here
# For example:
# from app.auth.jwt import admin_required
# router.dependencies.append(Depends(admin_required))