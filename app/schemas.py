from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CamCreate(BaseModel):
    name: str
    notify_helmet: Optional[bool] = True
    notify_vest: Optional[bool] = True
    notify_boots: Optional[bool] = True

class CamRead(BaseModel):
    id: int
    name: str
    owner_id: int
    notify_helmet: bool
    notify_vest: bool
    notify_boots: bool
    created_at: datetime

    class Config:
        orm_mode = True

class RegionDetection(BaseModel):
    position: str
    missing_items: List[str]

class DetectionIn(BaseModel):
    cam_id: int
    detections: List[RegionDetection]
    image: Optional[str] = None  # base64 encoded snapshot

class NotificationOut(BaseModel):
    id: int
    cam_id: int
    message: str
    image_path: Optional[str]
    timestamp: datetime

    class Config:
        orm_mode = True
