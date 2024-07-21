from functools import wraps
from fastapi import HTTPException, status, Depends
from .jwt import get_current_user

def admin_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = await get_current_user()
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        if current_user.get('role') != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin role required",
            )
        return await func(*args, **kwargs)
    return wrapper

def scheduler_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        current_user = await get_current_user()
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required",
            )
        if current_user.get('role') != "scheduler":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Scheduler role required",
            )
        return await func(*args, **kwargs)
    return wrapper