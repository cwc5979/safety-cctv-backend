from fastapi import APIRouter, Depends
from app.deps import get_current_user
from app.schemas import UserRead

router = APIRouter(prefix="/auth", tags=["auth"])
@router.get("/me", response_model=UserRead)
def read_current_user(user: dict = Depends(get_current_user)):
    return UserRead(id=user["uid"], email=user.get("email"))