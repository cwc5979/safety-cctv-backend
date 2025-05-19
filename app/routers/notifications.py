from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List

from app import crud, schemas
from app.database import get_db
from app.deps import get_current_user

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=List[schemas.NotificationRead])
def read_notifications(
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> List[schemas.NotificationRead]:
    return crud.get_user_notifications(session, user_id=current_user.id)

@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_notification(
    notification_id: int,
    session: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    note = crud.get_notification(session, notification_id)
    if not note or note.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    crud.delete_notification(session, notification_id)
    return None