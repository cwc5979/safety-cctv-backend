from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app import schemas, crud, utils, database

router = APIRouter()

@router.post("/register", response_model=schemas.UserRead)
def register(data: schemas.UserCreate, db: Session = Depends(database.get_db)):
    if crud.get_user_by_email(db, data.email):
        raise HTTPException(400, "이미 가입된 이메일입니다.")
    return crud.create_user(db, data)

@router.post("/login", response_model=schemas.Token)
def login(data: schemas.UserLogin, db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "인증 실패")
    access_token = utils.create_access_token({"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
