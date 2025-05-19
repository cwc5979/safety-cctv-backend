from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    project_id: str
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    cloud_sql_connection_name: str

    # JWT settings
    jwt_secret_key: str = Field(..., env="JWT_SECRET_KEY")
    jwt_algorithm: str = Field("HS256", env="JWT_ALGORITHM")
    jwt_access_token_expires: int = Field(30, env="JWT_ACCESS_TOKEN_EXPIRES")  # minutes

    # YOLO settings
    #  - 모델 파일(.pt)과 그 외 리소스를 담은 폴더 경로
    yolo_model_dir: str = Field("./models", env="YOLO_MODEL_DIR")
    #  - 이미지 저장 시 GCS를 쓰려면 버킷 이름, 아니면 로컬 저장
    gcs_bucket_name: Optional[str] = Field(None, env="GCS_BUCKET_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"

# 전역 settings 인스턴스
settings = Settings()
