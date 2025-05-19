from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.deps import get_current_user
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/protected", tags=["protected"], dependencies=[Depends(get_current_user)])
@router.get("/info", response_model=schemas.ProtectedInfo)
def get_protected_info(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    info = crud.get_protected_info(db, owner_id=user["uid"])
    if not info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Protected data not found")
    return info