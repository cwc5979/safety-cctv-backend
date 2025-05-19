from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field

# ----- User Schemas -----
class UserBase(SQLModel):
    email: str

    class Config:
        from_attributes = True

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    cams: List["CamRead"] = []  # related cameras
    notifications: List["NotificationRead"] = []  # related notifications


# ----- Cam Schemas -----
class CamBase(SQLModel):
    name: str
    helmet_alert: bool = True
    vest_alert: bool = True
    shoes_alert: bool = True

    class Config:
        from_attributes = True

class CamCreate(CamBase):
    owner_id: int

class CamRead(CamBase):
    id: int
    owner_id: int
    detections: List["DetectionRead"] = []


# ----- Detection Schemas -----
class DetectionBase(SQLModel):
    helmet: bool
    vest: bool
    shoes: bool
    coords: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class DetectionCreate(DetectionBase):
    cam_id: int

class DetectionRead(DetectionBase):
    id: int
    cam_id: int
    timestamp: datetime
    notifications: List["NotificationRead"] = []


# ----- Notification Schemas -----
class NotificationBase(SQLModel):
    is_read: bool = False

    class Config:
        from_attributes = True

class NotificationCreate(NotificationBase):
    user_id: int
    detection_id: int

class NotificationRead(NotificationBase):
    id: int
    user_id: int
    detection_id: int
    created_at: datetime

# ----- Protected Info Schema -----
class ProtectedInfo(SQLModel):
    id: int
    email: str

    class Config:
        from_attributes = True

# Resolve forward refs
UserRead.update_forward_refs()
CamRead.update_forward_refs()
DetectionRead.update_forward_refs()
NotificationRead.update_forward_refs()