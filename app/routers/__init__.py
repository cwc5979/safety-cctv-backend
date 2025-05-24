from fastapi import APIRouter
from .detect import router as detect_router

# 각 서브 라우터를 import
from .auth import router as auth_router
from .cams import router as cams_router
from .alerts import router as alerts_router
from .notifications import router as notifications_router
from .protected import router as protected_router

# 메인 API 라우터 생성
api_router = APIRouter()
api_router.include_router(detect_router)

# 서브 라우터 포함
api_router.include_router(auth_router)
api_router.include_router(cams_router)
api_router.include_router(alerts_router)
api_router.include_router(notifications_router)
api_router.include_router(protected_router)