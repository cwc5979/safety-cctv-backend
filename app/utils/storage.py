import os
import uuid
from datetime import datetime
from google.cloud import storage as gcs_storage
from app.config import settings

# 로컬 저장 시 사용할 폴더 (.gitignore에 이미 app/media/가 포함되어 있습니다)
LOCAL_MEDIA_DIR = os.path.join("app", "media", "detections")

def save_image(image_bytes: bytes, prefix: str = "") -> str:
    """
    이미지 바이트를 GCS 또는 로컬에 저장하고, 저장 경로를 반환합니다.
    - settings.gcs_bucket_name 이 설정되어 있으면 GCS에,
      아니면 app/media/detections/에 로컬 저장.
    :param image_bytes: JPEG 인코딩된 바이트
    :param prefix: 파일명 앞에 붙일 접두사 (예: cam ID)
    :return: "gs://버킷/..." 또는 "app/media/detections/... .jpg"
    """
    # 파일명 생성
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    filename = f"{timestamp}_{uuid.uuid4().hex}.jpg"
    # 1) GCS 저장
    if settings.gcs_bucket_name:
        client = gcs_storage.Client()
        bucket = client.bucket(settings.gcs_bucket_name)
        blob_name = f"{prefix}/{filename}" if prefix else filename
        blob = bucket.blob(blob_name)
        blob.upload_from_string(image_bytes, content_type="image/jpeg")
        return f"gs://{settings.gcs_bucket_name}/{blob_name}"
    # 2) 로컬 저장
    os.makedirs(LOCAL_MEDIA_DIR, exist_ok=True)
    target_dir = os.path.join(LOCAL_MEDIA_DIR, prefix) if prefix else LOCAL_MEDIA_DIR
    os.makedirs(target_dir, exist_ok=True)
    path = os.path.join(target_dir, filename)
    with open(path, "wb") as f:
        f.write(image_bytes)
    return path