from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    cams: List["Cam"] = Relationship(back_populates="owner")

class Cam(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(foreign_key="user.id")
    notify_helmet: bool = Field(default=True)
    notify_vest: bool = Field(default=True)
    notify_boots: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    owner: User = Relationship(back_populates="cams")

class Notification(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cam_id: int = Field(foreign_key="cam.id")
    message: str
    image_path: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
