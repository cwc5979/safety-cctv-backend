from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app import schemas, crud, utils, database

router = APIRouter()

@router.post("/detections/")
def handle_detection(
    payload: schemas.DetectionIn,
    db: Session = Depends(database.get_db)
):
    cam = crud.get_cam(db, payload.cam_id)
    if not cam:
        raise HTTPException(status_code=404, detail="Cam not found")

    # 각 영역(region)의 누락 항목을 순회하며 알림 생성
    for region in payload.detections:
        position = region.position
        for item in region.missing_items:
            message = f"{position}에서 {item} 미착용 감지됨"
            # 안전모
            if item == "안전모" and cam.notify_helmet:
                crud.create_notification(db, cam.id, message)
            # 조끼
            elif item == "조끼" and cam.notify_vest:
                crud.create_notification(db, cam.id, message)
            # 안전화
            elif item == "안전화" and cam.notify_boots:
                crud.create_notification(db, cam.id, message)
            # 기타 장비(예: 방진 마스크) 처리 시 Cam 모델 및 스키마에 notify_mask 필드를 추가하고 아래 조건을 활성화하세요.
            # elif item == "방진 마스크" and getattr(cam, "notify_mask", False):
            #     crud.create_notification(db, cam.id, message)

    return {"status": "ok"}

@router.get("/", response_model=list[schemas.NotificationOut])
def read_notifications(
    db: Session = Depends(database.get_db),
    user = Depends(utils.get_current_user),
    cam_id: int = None
):
    query = db.query(crud.models.Notification)
    # 특정 cam_id가 주어지면 필터링
    if cam_id:
        query = query.filter(crud.models.Notification.cam_id == cam_id)

    # 사용자 소유 장치의 알림만 반환하도록 추가할 경우 아래 로직을 반영하세요.
    # query = query.join(crud.models.Cam).filter(crud.models.Cam.owner_id == user.id)

    return query.all()
