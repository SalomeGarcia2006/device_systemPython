from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import get_db, create_tables

app = FastAPI()

# Crear las tablas al iniciar la aplicación
create_tables()

@app.get("/")
def root():
    return {"mensaje": "API con SQLAlchemy funcionando"}

@app.get("/test-db/")
def test_database(db: Session = Depends(get_db)):
    # Verificar que la conexión funciona
    try:
        # Ejecutar una consulta simple
        result = db.execute("SELECT 1")
        return {"estado": "Conexión exitosa", "resultado": result.scalar()}
    except Exception as e:
        return {"error": f"Error de conexión:{str(e)}"}