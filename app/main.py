from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.database import create_db_and_tables
from app.routers import api_router
from app.routers import cams, detections, notifications, detect

app = FastAPI(title="Safety CCTV Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # 개발 단계에서는 모든 출처 허용. 운영 시엔 프론트엔드 도메인으로 제한하세요.
    allow_credentials=True,
    allow_methods=["*"],            # GET, POST, PUT, DELETE... 모두 허용
    allow_headers=["*"],
)

app.include_router(cams.router)
app.include_router(detections.router)
app.include_router(notifications.router)
app.include_router(detect.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/media", StaticFiles(directory="app/media"), name="media")

# DB 생성/테이블 매핑
create_db_and_tables()

# 통합 라우터
app.include_router(api_router)

@app.get("/health", tags=["health"])
async def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    import os
    import uvicorn

    # Cloud Run이 주입하는 PORT 사용, 없으면 8080
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
