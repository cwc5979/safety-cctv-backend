from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str
    cams: List["Cam"] = Relationship(back_populates="owner")
    notifications: List["Notification"] = Relationship(back_populates="user")

class Cam(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="user.id")
    helmet_alert: bool = Field(default=True)
    vest_alert: bool = Field(default=True)
    shoes_alert: bool = Field(default=True)
    detections: List["Detection"] = Relationship(back_populates="cam")

class Detection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cam_id: int = Field(foreign_key="cam.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    helmet: bool
    vest: bool
    shoes: bool
    coords: str
    image_url: Optional[str] = None
    cam: "Cam" = Relationship(back_populates="detections")
    notifications: List["Notification"] = Relationship(back_populates="detection")

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    detection_id: int = Field(foreign_key="detection.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)
    detection: "Detection" = Relationship(back_populates="notifications")
    user: "User" = Relationship(back_populates="notifications")