import base64
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.deps import get_current_user
from app.database import get_db
from app import crud, schemas
from app.utils.notifier import send_notification

router = APIRouter(prefix="/alerts", tags=["alerts"])

@router.post("/", response_model=schemas.DetectionRead, status_code=status.HTTP_201_CREATED)
def create_alert(
    detection_in: schemas.DetectionCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> schemas.DetectionRead:
    cam = crud.get_cam(db, id=detection_in.cam_id)
    if not cam or cam.owner_id != user["uid"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized cam access")

    # 이미지 저장 처리
    if detection_in.image_url:
        media_dir = Path("app/media") / str(detection_in.cam_id)
        media_dir.mkdir(parents=True, exist_ok=True)
        ts_str = detection_in.timestamp.isoformat().replace(":", "-")
        with open(media_dir / f"{ts_str}.jpg", "wb") as f:
            f.write(base64.b64decode(detection_in.image_url))
        detection_in.image_url = f"/media/{detection_in.cam_id}/{ts_str}.jpg"

    # Detection 생성
    saved = crud.create_detection(
        db,
        cam_id=detection_in.cam_id,
        helmet=detection_in.helmet,
        vest=detection_in.vest,
        shoes=detection_in.shoes,
        coords=detection_in.coords,
        image_url=detection_in.image_url,
    )

    # FCM 토큰 조회 후 푸시 전송
    tokens = crud.get_user_tokens(db, user_id=user["uid"])
    if tokens:
        title = f"카메라 {cam.name}에서 안전 장비 미착용 감지"
        body = f"{detection_in.timestamp.isoformat()}에 미착용이 감지되었습니다."
        send_notification(
            tokens,
            title=title,
            body=body,
        )

    return saved

@router.get("/", response_model=List[schemas.DetectionRead])
def list_alerts(
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    sort_desc: bool = Query(True),
) -> List[schemas.DetectionRead]:
    # 사용자 소유 카메라 전체에서 탐지 데이터를 모아 반환
    return crud.get_detections_for_user(
        db, owner_id=user["uid"], limit=limit, offset=offset, sort_desc=sort_desc
    )
