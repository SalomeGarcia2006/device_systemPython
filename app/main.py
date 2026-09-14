from fastapi import FastAPI
from app.database import create_tables
from app.routes.user_routes import router as user_router

from app import models

create_tables()

app = FastAPI()
app.include_router(user_router)

