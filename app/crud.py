from sqlmodel import Session, select
from typing import List, Optional
from app.models import Cam, Detection, Notification
from sqlalchemy.orm import Session
from app.models import FCMToken

# Cam CRUD

def create_cam(
    session: Session,
    name: str,
    owner_id: int,
    helmet_alert: bool = True,
    vest_alert: bool = True,
    shoes_alert: bool = True,
) -> Cam:
    cam = Cam(
        name=name,
        owner_id=owner_id,
        helmet_alert=helmet_alert,
        vest_alert=vest_alert,
        shoes_alert=shoes_alert,
    )
    session.add(cam)
    session.commit()
    session.refresh(cam)
    return cam


def get_cams_for_user(session: Session, owner_id: int) -> List[Cam]:
    return session.exec(select(Cam).where(Cam.owner_id == owner_id)).all()

# Detection CRUD

def create_detection(
    session: Session,
    cam_id: int,
    helmet: bool,
    vest: bool,
    shoes: bool,
    coords: str,
    image_url: Optional[str] = None,
) -> Detection:
    det = Detection(
        cam_id=cam_id,
        helmet=helmet,
        vest=vest,
        shoes=shoes,
        coords=coords,
        image_url=image_url,
    )
    session.add(det)
    session.commit()
    session.refresh(det)
    return det


def get_detections_for_cam(session: Session, cam_id: int) -> List[Detection]:
    return session.exec(select(Detection).where(Detection.cam_id == cam_id)).all()

# Notification CRUD

def create_notification(session: Session, user_id: int, detection_id: int) -> Notification:
    note = Notification(user_id=user_id, detection_id=detection_id)
    session.add(note)
    session.commit()
    session.refresh(note)
    return note


def get_user_notifications(session: Session, user_id: int) -> List[Notification]:
    return session.exec(select(Notification).where(Notification.user_id == user_id)).all()


def get_notification(session: Session, notification_id: int) -> Optional[Notification]:
    return session.get(Notification, notification_id)


def delete_notification(session: Session, notification_id: int) -> None:
    note = session.get(Notification, notification_id)
    if note:
        session.delete(note)
        session.commit()

def save_user_token(db: Session, user_id: int, token: str) -> FCMToken:
    db_obj = FCMToken(user_id=user_id, token=token)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_user_tokens(db: Session, user_id: int) -> list[str]:
    tokens = db.query(FCMToken).filter(FCMToken.user_id == user_id).all()
    return [t.token for t in tokens]