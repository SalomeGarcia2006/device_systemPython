# Device Systems

API REST para administrar el inventario de dispositivos y sus préstamos. El sistema permite registrar usuarios, crear y consultar dispositivos, prestar un dispositivo a un usuario y registrar su devolución. La disponibilidad del dispositivo se actualiza automáticamente durante el ciclo del préstamo.

## Funcionalidades

* CRUD de usuarios con roles (`admin`, `support` y `user`) y estado activo.
* CRUD de dispositivos con número de serie único.
* Filtros y búsqueda de dispositivos por tipo, marca, disponibilidad o texto.
* Creación de préstamos validando que el usuario y el dispositivo existan.
* Bloqueo de préstamos cuando el dispositivo no está disponible.
* Devolución de préstamos y actualización automática de la disponibilidad.
* Consulta de préstamos por usuario, dispositivo o mediante información detallada.
* Documentación interactiva generada por FastAPI.

## Tecnologías y requisitos

* Python 3.10 o superior
* FastAPI `0.141.1`
* Uvicorn `0.52.4`
* SQLAlchemy `2.0.52`
* Pydantic y `email-validator`
* Alembic para migraciones
* SQLite

## Instalación

Desde la carpeta raíz del proyecto, crea y activa un entorno virtual:

### Windows PowerShell

```powershell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\venv\Scripts\Activate.ps1
```

Instala las dependencias del proyecto:

```powershell
pip install -r app/requeriments.txt
```

> El archivo de dependencias utilizado actualmente por la aplicación es `app/requeriments.txt`.

## Base de datos y migraciones

La aplicación utiliza SQLite por defecto y guarda la base de datos en `test.db` en la raíz del proyecto. La estructura se administra mediante Alembic; no se deben borrar bases de datos ni reiniciar el historial de migraciones.

Para aplicar las migraciones de Alembic de forma explícita:

```powershell
alembic upgrade head
```

Para consultar la revisión actual o revertir la última migración:

```powershell
alembic current
alembic downgrade -1
```

Las migraciones incluyen las tablas `users`, `devices` y `loans`. La cadena de relaciones es `users -> loans <- devices`.

## Ejecución

Inicia el servidor en modo desarrollo desde la raíz del proyecto:

```powershell
uvicorn app.main:app --reload
```

La API estará disponible en:

* API: http://127.0.0.1:8000
* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

Los endpoints de recursos requieren un JWT, salvo el registro y el login. La interfaz `/docs` permite autenticarse mediante el botón **Authorize** usando OAuth2 password flow y luego probar las operaciones protegidas.

## Configuración y autenticación

Copia `.env.example` como `.env` y configura una `SECRET_KEY` aleatoria que no se publique ni se incluya en el control de versiones:

```powershell
Copy-Item .env.example .env
```

`POST /auth/register` registra usuarios públicos como `user`. No permite crear administradores desde el exterior, porque aceptar `role=admin` en un registro público permitiría una escalada de privilegios. Las cuentas administrativas deben ser creadas por un administrador mediante `POST /users/`.

Para iniciar sesión, envía `username` (el correo) y `password` como formulario `application/x-www-form-urlencoded` a `POST /auth/login`. La respuesta contiene un JWT:

```json
{
  "access_token": "token_generado",
  "token_type": "bearer"
}
```

En Swagger, abre `POST /auth/login`, pulsa **Try it out** y completa el formulario OAuth2 así:

| Campo           | Valor                               |
| --------------- | ----------------------------------- |
| `grant_type`    | `password`                          |
| `username`      | El correo usado durante el registro |
| `password`      | La contraseña registrada            |
| `scope`         | Déjalo vacío                        |
| `client_id`     | Déjalo vacío                        |
| `client_secret` | Déjalo vacío                        |

El campo `username` representa el correo electrónico, aunque Swagger lo nombre `username`. `grant_type` debe ser exactamente `password`. Si se envía JSON en lugar de un formulario, el endpoint devuelve `422`.

Después de obtener el token, pulsa **Authorize** en Swagger y pega el token en el campo de autenticación. Swagger agregará automáticamente el prefijo `Bearer` a las peticiones protegidas. También puedes enviar manualmente:

```text
Authorization: Bearer <access_token>
```

`GET /auth/me` devuelve el usuario autenticado sin `password` ni `hashed_password`. Un token ausente, inválido, expirado o mal formado devuelve `401`; un usuario autenticado sin el rol requerido devuelve `403`.

Los roles disponibles son `admin`, `support` y `user`.

* `admin` puede administrar usuarios y dispositivos.
* `support` puede operar dispositivos y préstamos.
* `user` puede consultar recursos autenticados y crear préstamos para su propio usuario.

## CORS, middleware y límites

En desarrollo se permiten los orígenes `http://localhost:5173` y `http://localhost:3000`, con credenciales, métodos y headers habilitados.

No se usa `allow_origins=["*"]` porque el navegador no permite combinar un origen comodín con `allow_credentials=True`. En producción se deben configurar orígenes explícitos y confiables.

El middleware global registra el método, la ruta, el estado y la duración de cada petición. También agrega:

* `X-App-Name`
* `X-Process-Time`
* `X-Request-ID`

Si el cliente envía `X-Request-ID`, se conserva; de lo contrario, se genera uno.

SlowAPI aplica estos límites por dirección IP:

| Endpoint              | Límite        |
| --------------------- | ------------- |
| `POST /auth/login`    | 5 por minuto  |
| `POST /auth/register` | 3 por minuto  |
| `GET /users/`         | 30 por minuto |
| `POST /loans/`        | 10 por minuto |

Al superar un límite, la API devuelve `429 Too Many Requests`.

## Endpoints

### Usuarios

| Método   | Endpoint                 | Descripción                        |
| -------- | ------------------------ | ---------------------------------- |
| `GET`    | `/users/`                | Lista todos los usuarios.          |
| `GET`    | `/users/{user_id}`       | Consulta un usuario por ID.        |
| `GET`    | `/users/{user_id}/loans` | Lista los préstamos de un usuario. |
| `POST`   | `/users/`                | Crea un usuario.                   |
| `PUT`    | `/users/{user_id}`       | Reemplaza los datos de un usuario. |
| `PATCH`  | `/users/{user_id}`       | Actualiza parcialmente un usuario. |
| `DELETE` | `/users/{user_id}`       | Elimina un usuario.                |

Roles permitidos: `admin`, `support` y `user`. El nombre debe tener entre 3 y 100 caracteres y el correo debe ser válido.

Las operaciones de administración de usuarios requieren el rol `admin`.

### Dispositivos

| Método   | Endpoint                     | Descripción                             |
| -------- | ---------------------------- | --------------------------------------- |
| `GET`    | `/devices/`                  | Lista dispositivos y admite filtros.    |
| `GET`    | `/devices/{device_id}`       | Consulta un dispositivo por ID.         |
| `GET`    | `/devices/{device_id}/loans` | Lista los préstamos de un dispositivo.  |
| `POST`   | `/devices/`                  | Crea un dispositivo. Devuelve `201`.    |
| `PUT`    | `/devices/{device_id}`       | Reemplaza los datos del dispositivo.    |
| `PATCH`  | `/devices/{device_id}`       | Actualiza parcialmente un dispositivo.  |
| `DELETE` | `/devices/{device_id}`       | Elimina un dispositivo. Devuelve `204`. |

Filtros disponibles en `GET /devices/`:

* `device_type`: filtra por tipo de dispositivo.
* `is_available`: filtra por disponibilidad (`true` o `false`).
* `brand`: filtra por marca.
* `search`: busca en nombre, número de serie, tipo y marca.

Ejemplo:

```text
/devices/?is_available=true&brand=Dell&search=laptop
```

### Préstamos

| Método  | Endpoint                  | Descripción                                          |
| ------- | ------------------------- | ---------------------------------------------------- |
| `GET`   | `/loans/`                 | Lista préstamos y admite filtros.                    |
| `GET`   | `/loans/details`          | Lista préstamos con datos del usuario y dispositivo. |
| `GET`   | `/loans/{loan_id}`        | Consulta un préstamo por ID.                         |
| `POST`  | `/loans/`                 | Crea un préstamo. Devuelve `201`.                    |
| `PATCH` | `/loans/{loan_id}/return` | Registra la devolución.                              |

Filtros disponibles en `GET /loans/`:

* `status`
* `user_email`
* `device_type`

Los estados utilizados por el sistema son `active` y `returned`.

Las rutas protegidas requieren autenticación. La consulta detallada y la devolución requieren los roles `admin` o `support`.

## Ejemplos de uso

### Crear un usuario

```json
{
  "name": "Ana García",
  "email": "ana.garcia@example.com",
  "role": "user",
  "is_active": true
}
```

### Crear un dispositivo

```json
{
  "name": "Laptop Latitude 5420",
  "serial_number": "DL5420-001",
  "device_type": "laptop",
  "brand": "Dell",
  "is_available": true
}
```

### Crear un préstamo

Después de crear el usuario y el dispositivo, utiliza sus IDs:

```json
{
  "user_id": 1,
  "device_id": 1
}
```

También puedes probar el flujo desde Swagger UI o con `curl`:

```powershell
curl.exe -X POST http://127.0.0.1:8000/loans/ -H "Content-Type: application/json" -d "{\"user_id\":1,\"device_id\":1}"
curl.exe -X PATCH http://127.0.0.1:8000/loans/1/return
```

## Estructura principal

```text
app/
├── main.py                         # Configuración y registro de routers
├── database.py                     # Motor, sesiones y conexión a la base de datos
├── models/                         # Modelos SQLAlchemy
│   ├── user_model.py
│   ├── device_model.py
│   └── loan_model.py
├── schemas/                        # Validación Pydantic
├── routes/                         # Endpoints de la API
│   ├── user_routes.py
│   ├── device_routes.py
│   └── loan_routes.py
└── services/                       # Lógica de negocio
    ├── user_service.py
    ├── device_service.py
    └── loan_service.py

alembic/
└── versions/                       # Historial de migraciones
```

## Respuestas y errores frecuentes

* `200`: operación exitosa.
* `201`: usuario, dispositivo o préstamo creado.
* `204`: dispositivo eliminado correctamente.
* `400`: número de serie duplicado.
* `404`: recurso, usuario o dispositivo no encontrado.
* `409`: dispositivo no disponible, préstamo ya devuelto o dispositivo con préstamos asociados.
* `422`: datos enviados no válidos según los esquemas Pydantic.
* `401`: falta autenticación o el JWT no es válido.
* `403`: el usuario autenticado no tiene permisos suficientes.
* `429`: se superó el límite de solicitudes.

Las contraseñas se almacenan únicamente como hashes bcrypt mediante Passlib. Nunca se guarda ni se devuelve la contraseña original.

## Evidencias

Agrega aquí las capturas o evidencias reales de Swagger, login, rutas protegidas, CORS, headers y rate limiting cuando estén disponibles.

No se incluyen capturas inventadas en el repositorio.
