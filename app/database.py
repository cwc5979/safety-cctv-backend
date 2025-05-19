from sqlmodel import SQLModel
from sqlalchemy import create_engine
from app.config import settings
from app.models import Cam, Detection, Notification

# DATABASE_URL 직접 구성 (public IP 직결)
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{settings.db_user}:{settings.db_password}"
    f"@{settings.db_host}:{settings.db_port}"
    f"/{settings.db_name}"
)

engine = create_engine(DATABASE_URL, echo=True) 

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    from sqlalchemy.orm import Session
    with Session(engine) as session:
        yield session