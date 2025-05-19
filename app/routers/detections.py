from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/detections", tags=["detections"])

@router.post("/", response_model=schemas.DetectionRead, status_code=status.HTTP_201_CREATED)
def create_detection(
    det_in: schemas.DetectionCreate,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> schemas.DetectionRead:
    # Optionally verify cam ownership...
    return crud.create_detection(
        session,
        cam_id=det_in.cam_id,
        helmet=det_in.helmet,
        vest=det_in.vest,
        shoes=det_in.shoes,
        coords=det_in.coords,
        image_url=det_in.image_url,
    )

@router.get("/", response_model=List[schemas.DetectionRead])
def read_detections(
    cam_id: int,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> List[schemas.DetectionRead]:
    # Optionally verify cam ownership...
    return crud.get_detections_for_cam(session, cam_id)