import os
from pydantic import BaseSettings

SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class Settings(BaseSettings):
    DATABASE_URL: str            # ex. postgresql+psycopg2://user:pw@/db?host=/cloudsql/INSTANCE
    CLOUD_SQL_INSTANCE: str      # ex. project:region:instance
    GCP_PROJECT: str
    PUBSUB_TOPIC: str = "detection-events"
    GCS_BUCKET: str
    FCM_CREDENTIALS_SECRET: str  # Secret Manager 이름
    class Config:
        env_file = ".env"
