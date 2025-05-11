from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app import schemas, crud, utils, database

router = APIRouter()

@router.post("/", response_model=schemas.CamRead)
def create_cam(data: schemas.CamCreate,
               db: Session = Depends(database.get_db),
               user = Depends(utils.get_current_user)):
    return crud.create_cam(db, user.id, data)

@router.get("/", response_model=list[schemas.CamRead])
def read_cams(db: Session = Depends(database.get_db),
              user = Depends(utils.get_current_user)):
    return db.query(crud.models.Cam).filter(crud.models.Cam.owner_id == user.id).all()

@router.patch("/{cam_id}", response_model=schemas.CamRead)
def update_cam(cam_id: int, data: schemas.CamCreate,
               db: Session = Depends(database.get_db),
               user = Depends(utils.get_current_user)):
    cam = crud.get_cam(db, cam_id)
    if cam.owner_id != user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "권한 없음")
    for k, v in data.dict().items():
        setattr(cam, k, v)
    db.add(cam)
    db.commit()
    db.refresh(cam)
    return cam
