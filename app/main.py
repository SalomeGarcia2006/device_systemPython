from fastapi import FastAPI

from app.database import create_tables

from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# Crear las tablas si no existen
create_tables()

app = FastAPI(
    title="Device Systems API",
    description="API para gestión de usuarios, dispositivos y préstamos.",
    version="1.0.0",
)

# Registrar routers
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)