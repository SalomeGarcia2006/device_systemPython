import logging
import time
from uuid import uuid4

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.core.rate_limit import limiter
from app.routes.auth_routes import router as auth_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.routes.user_routes import router as user_router


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("device_systems.requests")

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="3.0.0",
    openapi_tags=[
        {"name": "Auth", "description": "Registro, inicio de sesión y perfil autenticado."},
        {"name": "Users", "description": "Administración de usuarios."},
        {"name": "Devices", "description": "Inventario de dispositivos."},
        {"name": "Loans", "description": "Préstamos y devoluciones."},
        {"name": "Security", "description": "Controles transversales de seguridad."},
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.middleware("http")
async def request_observability(request: Request, call_next):
    request_id = request.headers.get("X-Request-ID", uuid4().hex)
    started_at = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - started_at
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-Request-ID"] = request_id
    logger.info(
        "request_id=%s method=%s path=%s status=%s process_time=%.4fs",
        request_id,
        request.method,
        request.url.path,
        response.status_code,
        process_time,
    )
    return response


app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)