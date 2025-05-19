from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/cams", tags=["cams"])

@router.post("/", response_model=schemas.CamRead, status_code=status.HTTP_201_CREATED)
def create_cam(
    cam_in: schemas.CamCreate,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> schemas.CamRead:
    return crud.create_cam(
        session,
        name=cam_in.name,
        owner_id=current_user.id,
        helmet_alert=cam_in.helmet_alert,
        vest_alert=cam_in.vest_alert,
        shoes_alert=cam_in.shoes_alert,
    )

@router.get("/", response_model=List[schemas.CamRead])
def read_cams(
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> List[schemas.CamRead]:
    return crud.get_cams_for_user(session, owner_id=current_user.id)