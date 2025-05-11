from sqlalchemy.orm import Session
from app import models, schemas, utils

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = utils.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not utils.verify_password(password, user.hashed_password):
        return None
    return user

def create_cam(db: Session, owner_id: int, cam: schemas.CamCreate):
    db_cam = models.Cam(owner_id=owner_id, **cam.dict())
    db.add(db_cam)
    db.commit()
    db.refresh(db_cam)
    return db_cam

def get_cam(db: Session, cam_id: int):
    return db.query(models.Cam).filter(models.Cam.id == cam_id).first()

def create_notification(db: Session, cam_id: int, message: str, image_path: str = None):
    notif = models.Notification(cam_id=cam_id, message=message, image_path=image_path)
    db.add(notif)
    db.commit()
    db.refresh(notif)
    return notif
