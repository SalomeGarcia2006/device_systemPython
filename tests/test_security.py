import os
from pathlib import Path

TEST_DB = Path("security_test.db")
if TEST_DB.exists():
    TEST_DB.unlink()
os.environ["DATABASE_URL"] = "sqlite:///./security_test.db"
os.environ["SECRET_KEY"] = "test-secret-that-is-not-used-in-production"
os.environ["ALGORITHM"] = "HS256"
os.environ["ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"

from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.main import app
from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.services.auth_service import register_user

Base.metadata.create_all(bind=engine)
client = TestClient(app)


def register(payload):
    return client.post("/auth/register", json=payload)


def login(email, password):
    response = client.post("/auth/login", data={"username": email, "password": password})
    assert response.status_code == 200
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


def test_security_flow():
    admin = {"name": "Admin Test", "email": "admin@example.com", "password": "AdminPass123", "role": "admin"}
    response = register(admin)
    assert response.status_code == 201
    assert "hashed_password" not in response.json()

    weak = register({**admin, "email": "weak@example.com", "password": "weak"})
    assert weak.status_code == 422
    duplicate = register(admin)
    assert duplicate.status_code == 409

    db = SessionLocal()
    admin_user = db.query(User).filter(User.email == "admin@example.com").first()
    assert admin_user is not None
    admin_user.role = "admin"
    db.commit()
    try:
        assert register_user(db, UserRegister(name="Support Test", email="support@example.com", password="SupportPass123", role="support"))
        assert register_user(db, UserRegister(name="User Test", email="user@example.com", password="UserPass123", role="user"))
    finally:
        db.close()

    admin_headers = login("admin@example.com", "AdminPass123")
    user_headers = login("user@example.com", "UserPass123")
    assert client.post("/auth/login", data={"username": "admin@example.com", "password": "WrongPass123"}).status_code == 401
    assert client.get("/auth/me", headers=admin_headers).status_code == 200
    assert client.get("/users/").status_code == 401
    assert client.get("/users/", headers={"Authorization": "Bearer invalid"}).status_code == 401

    device = {"name": "Laptop Test", "serial_number": "TEST-001", "device_type": "laptop", "brand": "Dell"}
    assert client.post("/devices/", json=device, headers=user_headers).status_code == 403
    created = client.post("/devices/", json=device, headers=admin_headers)
    assert created.status_code == 201
    assert client.delete(f"/devices/{created.json()['id']}", headers=user_headers).status_code == 403

    request_id = "verification-request-id"
    protected = client.get("/users/", headers={**admin_headers, "X-Request-ID": request_id})
    assert protected.status_code == 200
    assert protected.headers["X-App-Name"] == "device_systems"
    assert protected.headers["X-Request-ID"] == request_id
    assert "X-Process-Time" in protected.headers

    cors = client.options("/users/", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"})
    assert cors.status_code == 200
    assert cors.headers["access-control-allow-origin"] == "http://localhost:5173"

    register({"name": "Rate Test 1", "email": "rate1@example.com", "password": "RatePass123", "role": "user"})
    register({"name": "Rate Test 2", "email": "rate2@example.com", "password": "RatePass123", "role": "user"})
    rate_response = register({"name": "Rate Test 3", "email": "rate3@example.com", "password": "RatePass123", "role": "user"})
    assert rate_response.status_code == 429

    schema = client.get("/openapi.json").json()
    assert schema["info"]["version"] == "3.0.0"
    assert "/auth/login" in schema["paths"]
    assert "OAuth2PasswordBearer" in schema["components"]["securitySchemes"]