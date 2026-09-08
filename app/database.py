from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# Configuración de la base de datos
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Motor de base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base para modelos
class Base(DeclarativeBase):
    pass

# Función para crear tablas
def create_tables():
    Base.metadata.create_all(bind=engine)

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()