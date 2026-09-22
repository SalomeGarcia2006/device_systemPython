import os

from dotenv import load_dotenv


load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def validate_security_settings() -> None:
    """Verifica que la aplicación no inicie JWT sin una clave configurada."""
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY debe estar configurada en el archivo .env")