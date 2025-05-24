from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.deps import get_db, get_current_user
from app.schemas import User

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/me/fcm-token")
def update_fcm_token(
    fcm_token: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    statement = select(User).where(User.firebase_uid == current_user.firebase_uid)
    user = db.exec(statement).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.fcm_token = fcm_token
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"result": "ok"}
