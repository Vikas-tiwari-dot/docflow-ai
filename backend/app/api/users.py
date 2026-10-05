from fastapi import APIRouter, Depends
from app.core.deps import get_current_user
from app.schemas.auth import UserResponse
router=APIRouter(prefix="/api/users",tags=["Users"])
@router.get("/me",response_model=UserResponse)
def me(user=Depends(get_current_user)): return user
