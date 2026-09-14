# Device Systems

API REST desarrollada con FastAPI para administrar usuarios mediante SQLite y SQLAlchemy.

## Tecnologías

- Python 3.10+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- SQLite

## Instalación

Desde la carpeta raíz del proyecto, crea y activa el entorno virtual:

### Windows PowerShell

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

Instala las dependencias:

```powershell
pip install -r app/requeriments.txt
```

## Ejecución

Inicia el servidor en modo desarrollo:

```powershell
uvicorn app.main:app --reload
```

La API estará disponible en:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

La base de datos SQLite `test.db` se crea automáticamente al iniciar la aplicación.

## Endpoints de usuarios

| Método | Endpoint | Descripción |
|---|---|---|
| `GET` | `/users/` | Lista todos los usuarios |
| `GET` | `/users/{user_id}` | Consulta un usuario por ID |
| `POST` | `/users/` | Crea un usuario |
| `PUT` | `/users/{user_id}` | Reemplaza todos los datos de un usuario |
| `PATCH` | `/users/{user_id}` | Actualiza parcialmente un usuario |
| `DELETE` | `/users/{user_id}` | Elimina un usuario |

## Ejemplo de usuario

```json
{
	"name": "Ana García",
	"email": "ana.garcia@example.com",
	"role": "user",
	"is_active": true
}
```

Los roles permitidos son `admin`, `support` y `user`. El campo `name` debe tener entre 3 y 100 caracteres y el correo debe ser válido.

## Estructura principal

```text
app/
├── database.py              # Conexión y sesiones SQLAlchemy
├── main.py                  # Configuración de FastAPI
├── models.py                # Modelos de base de datos
├── routes/user_routes.py    # Endpoints de usuarios
├── schemas/user_schema.py   # Validación de entrada y salida
└── services/user_service.py # Lógica CRUD
```

## Respuestas y errores

- `200`: operación exitosa.
- `404`: usuario no encontrado.
- `422`: datos enviados no válidos.

La documentación interactiva en `/docs` permite probar cada endpoint directamente desde el navegador.

