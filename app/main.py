from fastapi import FastAPI

from app.routes.user_routes import router as user_router


app = FastAPI(
    title="Device Systems API",
    description="API REST para gestión de usuarios",
    version="1.0"
)


app.include_router(user_router)