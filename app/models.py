from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    cams: List["Cam"] = Relationship(back_populates="owner")
    notifications: List["Notification"] = Relationship(back_populates="user")
    fcm_tokens: List["FCMToken"] = Relationship(back_populates="user")

class Cam(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="user.id")
    owner: User = Relationship(back_populates="cams")
    detections: List["Detection"] = Relationship(back_populates="cam")
    helmet_alert: bool = Field(default=True)
    vest_alert: bool = Field(default=True)
    shoes_alert: bool = Field(default=True)

class Detection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cam_id: int = Field(foreign_key="cam.id")
    cam: Cam = Relationship(back_populates="detections")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    helmet: bool
    vest: bool
    shoes: bool
    coords: str
    image_url: Optional[str] = None
    notifications: List["Notification"] = Relationship(back_populates="detection")

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    detection_id: int = Field(foreign_key="detection.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)
    user: User = Relationship(back_populates="notifications")
    detection: Detection = Relationship(back_populates="notifications")

class FCMToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    token: str
    user: User = Relationship(back_populates="fcm_tokens")

fcm_tokens: List["FCMToken"] = Relationship(back_populates="user")