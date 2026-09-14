from sqlalchemy import create_engine, inspect, text
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

    # `create_all` no modifica tablas que ya existen. Estas migraciones
    # pequeñas mantienen compatible la base SQLite creada por versiones
    # anteriores de la API.
    if engine.dialect.name != "sqlite":
        return

    columns = {column["name"] for column in inspect(engine).get_columns("users")}
    with engine.begin() as connection:
        if "role" not in columns:
            connection.execute(
                text("ALTER TABLE users ADD COLUMN role VARCHAR NOT NULL DEFAULT 'user'")
            )
        if "created_at" not in columns:
            connection.execute(text("ALTER TABLE users ADD COLUMN created_at DATETIME"))
            connection.execute(
                text("UPDATE users SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL")
            )

# Función para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()