from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.deps import get_current_user
from app.database import get_db
from app.schemas import FCMTokenCreate
from app import crud

router = APIRouter(
    prefix="/tokens",
    tags=["tokens"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def register_token(
    token_in: FCMTokenCreate,
    user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return crud.save_user_token(db, user["uid"], token_in.token)