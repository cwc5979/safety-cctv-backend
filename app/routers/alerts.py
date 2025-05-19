import base64
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.deps import get_current_user
from app.database import get_db
from app import crud, schemas
from app.utils.notifier import send_notification

router = APIRouter(prefix="/alerts", tags=["alerts"], dependencies=[Depends(get_current_user)])
@router.post("/", response_model=schemas.DetectionRead, status_code=status.HTTP_201_CREATED)
def create_alert(detection_in: schemas.DetectionCreate, user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    cam = crud.get_cam(db, id=detection_in.cam_id)
    if not cam or cam.owner_id != user["uid"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized cam access")
    if detection_in.image_url:
        media_dir = Path("app/media") / str(detection_in.cam_id)
        media_dir.mkdir(parents=True, exist_ok=True)
        ts_str = detection_in.timestamp.isoformat().replace(":", "-")
        with open(media_dir / f"{ts_str}.jpg", "wb") as f:
            f.write(base64.b64decode(detection_in.image_url))
        detection_in.image_url = f"/media/{detection_in.cam_id}/{ts_str}.jpg"
    saved = crud.create_detection(db, detection=detection_in)
    tokens = crud.get_user_tokens(db, owner_id=user["uid"])
    send_notification(tokens, "안전 장비 미착용 감지", f"카메라 {detection_in.cam_id}에서 미착용이 감지되었습니다.", saved.image_url)
    return saved
@router.get("/", response_model=List[schemas.DetectionRead])
def list_alerts(user: dict = Depends(get_current_user), db: Session = Depends(get_db), limit: int = Query(20, ge=1), offset: int = Query(0, ge=0), sort_desc: bool = Query(True)):
    return crud.get_detections_for_user(db, owner_id=user["uid"], limit=limit, offset=offset, sort_desc=sort_desc)
