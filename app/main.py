from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
from app.database import engine, create_db_and_tables, get_db
from app.routers import auth, cams, notifications

app = FastAPI()

create_db_and_tables()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(cams.router, prefix="/cams", tags=["cams"])
app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])

app.mount("/media", StaticFiles(directory="app/media"), name="media")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    schema = get_openapi(
        title="건설현장 안전 CCTV API",
        version="1.0.0",
        description="…",
        routes=app.routes,
    )
    # 기존 OAuth2PasswordBearer 정의를 지우고, HTTP bearerAuth로 재정의
    schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    # 모든 경로에 bearerAuth 적용
    for path in schema["paths"].values():
        for method in path.values():
            method.setdefault("security", []).append({"bearerAuth": []})
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
