from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import uuid
import os
import subprocess
import json
import sys

router = APIRouter(prefix="/detect", tags=["detect"])

AI_PY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../yolov5/ai.py"))
INPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../input"))
RESULT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../result"))

@router.post("/")
async def detect_image(file: UploadFile = File(...)):
    os.makedirs(INPUT_DIR, exist_ok=True)
    file_ext = os.path.splitext(file.filename)[1]
    save_name = f"{uuid.uuid4().hex}{file_ext}"
    save_path = os.path.join(INPUT_DIR, save_name)
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # ai.py 일괄 처리 버전: 모든 input/ 처리
    try:
        subprocess.run([sys.executable, AI_PY_PATH], check=True)
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="AI 감지 중 오류 발생")

    result_json_path = os.path.join(RESULT_DIR, f"{os.path.splitext(save_name)[0]}.json")
    if not os.path.exists(result_json_path):
        raise HTTPException(status_code=404, detail="결과 json 파일이 생성되지 않았습니다.")

    with open(result_json_path, "r", encoding="utf-8") as f:
        result_data = json.load(f)

    return result_data