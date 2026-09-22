# Device Systems

API REST para administrar el inventario de dispositivos y sus prÃ©stamos. El
sistema permite registrar usuarios, crear y consultar dispositivos, prestar un
dispositivo a un usuario y registrar su devoluciÃ³n. La disponibilidad del
dispositivo se actualiza automÃ¡ticamente durante el ciclo del prÃ©stamo.

## Funcionalidades

- CRUD de usuarios con roles (`admin`, `support` y `user`) y estado activo.
- CRUD de dispositivos con nÃºmero de serie Ãºnico.
- Filtros y bÃºsqueda de dispositivos por tipo, marca, disponibilidad o texto.
- CreaciÃ³n de prÃ©stamos validando que el usuario y el dispositivo existan.
- Bloqueo de prÃ©stamos cuando el dispositivo no estÃ¡ disponible.
- DevoluciÃ³n de prÃ©stamos y actualizaciÃ³n automÃ¡tica de la disponibilidad.
- Consulta de prÃ©stamos por usuario, dispositivo o mediante informaciÃ³n detallada.
- DocumentaciÃ³n interactiva generada por FastAPI.

## TecnologÃ­as y requisitos

- Python 3.10 o superior
- FastAPI `0.141.1`
- Uvicorn `0.52.4`
- SQLAlchemy `2.0.52`
- Pydantic y `email-validator`
- Alembic para migraciones
- SQLite

## InstalaciÃ³n

Desde la carpeta raÃ­z del proyecto, crea y activa un entorno virtual:

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

> El archivo de dependencias utilizado actualmente por la aplicaciÃ³n es
> `app/requeriments.txt`.

## Base de datos y migraciones

La aplicaciÃ³n utiliza SQLite por defecto y guarda la base de datos en `test.db`
en la raÃ­z del proyecto. La estructura se administra mediante Alembic; no se
deben borrar bases de datos ni reiniciar el historial de migraciones.

Para aplicar las migraciones de Alembic de forma explÃ­cita:

```powershell
alembic upgrade head
```

Para consultar la revisiÃ³n actual o revertir la Ãºltima migraciÃ³n:

```powershell
alembic current
alembic downgrade -1
```

Las migraciones incluyen las tablas `users`, `devices` y `loans`. La cadena de
relaciones es `users -> loans <- devices`.

## EjecuciÃ³n

Inicia el servidor en modo desarrollo desde la raÃ­z del proyecto:

```powershell
uvicorn app.main:app --reload
```

La API estarÃ¡ disponible en:

- API: <http://127.0.0.1:8000>
- Swagger UI: <http://127.0.0.1:8000/docs>
- ReDoc: <http://127.0.0.1:8000/redoc>

Los endpoints de recursos requieren un JWT salvo el registro y el login. La
interfaz `/docs` permite autenticarse mediante el botÃ³n **Authorize** usando
OAuth2 password flow y luego probar las operaciones protegidas.

## ConfiguraciÃ³n y autenticaciÃ³n

Copia `.env.example` como `.env` y configura una `SECRET_KEY` aleatoria que no
se publique ni se incluya en el control de versiones:

```powershell
Copy-Item .env.example .env
```

`POST /auth/register` registra usuarios pÃºblicos como `user`. No permite
crear administradores desde el exterior, porque aceptar `role=admin` en un
registro pÃºblico permitirÃ­a una escalada de privilegios. Las cuentas
administrativas deben ser creadas por un administrador mediante `POST /users/`.

Para iniciar sesiÃ³n, envÃ­a `username` (el correo) y `password` como formulario
`application/x-www-form-urlencoded` a `POST /auth/login`. La respuesta contiene
un JWT:

```json
{
  "access_token": "token_generado",
  "token_type": "bearer"
}
```

En Swagger, abre `POST /auth/login`, pulsa **Try it out** y completa el
formulario OAuth2 asÃ­:

| Campo | Valor |
|---|---|
| `grant_type` | `password` |
| `username` | El correo usado durante el registro |
| `password` | La contraseÃ±a registrada |
| `scope` | DÃ©jalo vacÃ­o |
| `client_id` | DÃ©jalo vacÃ­o |
| `client_secret` | DÃ©jalo vacÃ­o |

El campo `username` representa el correo electrÃ³nico, aunque Swagger lo
nombre `username`. `grant_type` debe ser exactamente `password`. Si se envÃ­a
JSON en lugar de un formulario, el endpoint devuelve `422`.

DespuÃ©s de obtener el token, pulsa **Authorize** en Swagger y pega el token
en el campo de autenticaciÃ³n. Swagger agregarÃ¡ automÃ¡ticamente el prefijo
`Bearer` a las peticiones protegidas. TambiÃ©n puedes enviar manualmente:

```text
Authorization: Bearer <access_token>
```

`GET /auth/me` devuelve el usuario autenticado sin `password` ni
`hashed_password`. Un token ausente, inválido, expirado o mal formado devuelve
`401`; un usuario autenticado sin el rol requerido devuelve `403`.

Los roles disponibles son `admin`, `support` y `user`. `admin` puede
administrar usuarios y dispositivos; `support` puede operar dispositivos y
prÃ©stamos; `user` puede consultar recursos autenticados y crear prÃ©stamos para
su propio usuario.

## CORS, middleware y lÃ­mites

En desarrollo se permiten los orÃ­genes `http://localhost:5173` y
`http://localhost:3000`, con credenciales, mÃ©todos y headers habilitados. No se
usa `allow_origins=["*"]` porque el navegador no permite combinar un origen
comodin con `allow_credentials=True`; en producciÃ³n se deben configurar
orÃ­genes explÃ­citos y confiables.

El middleware global registra mÃ©todo, ruta, estado y duraciÃ³n de cada peticiÃ³n.
TambiÃ©n agrega `X-App-Name`, `X-Process-Time` y `X-Request-ID`. Si el cliente
envÃ­a `X-Request-ID`, se conserva; de lo contrario se genera uno.

SlowAPI aplica estos lÃ­mites por direcciÃ³n IP:

| Endpoint | LÃ­mite |
|---|---|
| `POST /auth/login` | 5 por minuto |
| `POST /auth/register` | 3 por minuto |
| `GET /users/` | 30 por minuto |
| `POST /loans/` | 10 por minuto |

Al superar un lÃ­mite la API devuelve `429 Too Many Requests`.

## Endpoints

### Usuarios

| MÃ©todo | Endpoint | DescripciÃ³n |
|---|---|---|
| `GET` | `/users/` | Lista todos los usuarios. |
| `GET` | `/users/{user_id}` | Consulta un usuario por ID. |
| `GET` | `/users/{user_id}/loans` | Lista los prÃ©stamos de un usuario. |
| `POST` | `/users/` | Crea un usuario. |
| `PUT` | `/users/{user_id}` | Reemplaza los datos de un usuario. |
| `PATCH` | `/users/{user_id}` | Actualiza parcialmente un usuario. |
| `DELETE` | `/users/{user_id}` | Elimina un usuario. |

Roles permitidos: `admin`, `support` y `user`. El nombre debe tener entre 3 y
100 caracteres y el correo debe ser vÃ¡lido.

Las operaciones de administraciÃ³n de usuarios requieren el rol `admin`.

### Dispositivos

| MÃ©todo | Endpoint | DescripciÃ³n |
|---|---|---|
| `GET` | `/devices/` | Lista dispositivos y admite filtros. |
| `GET` | `/devices/{device_id}` | Consulta un dispositivo por ID. |
| `GET` | `/devices/{device_id}/loans` | Lista los prÃ©stamos de un dispositivo. |
| `POST` | `/devices/` | Crea un dispositivo. Devuelve `201`. |
| `PUT` | `/devices/{device_id}` | Reemplaza los datos del dispositivo. |
| `PATCH` | `/devices/{device_id}` | Actualiza parcialmente un dispositivo. |
| `DELETE` | `/devices/{device_id}` | Elimina un dispositivo. Devuelve `204`. |

Filtros disponibles en `GET /devices/`:

- `device_type`: filtra por tipo de dispositivo.
- `is_available`: filtra por disponibilidad (`true` o `false`).
- `brand`: filtra por marca.
- `search`: busca en nombre, nÃºmero de serie, tipo y marca.

Ejemplo: `/devices/?is_available=true&brand=Dell&search=laptop`.

### PrÃ©stamos

| MÃ©todo | Endpoint | DescripciÃ³n |
|---|---|---|
| `GET` | `/loans/` | Lista prÃ©stamos y admite filtros. |
| `GET` | `/loans/details` | Lista prÃ©stamos con datos del usuario y dispositivo. |
| `GET` | `/loans/{loan_id}` | Consulta un prÃ©stamo por ID. |
| `POST` | `/loans/` | Crea un prÃ©stamo. Devuelve `201`. |
| `PATCH` | `/loans/{loan_id}/return` | Registra la devoluciÃ³n. |

Filtros disponibles en `GET /loans/`: `status`, `user_email` y `device_type`.
Los estados utilizados por el sistema son `active` y `returned`.

Las rutas protegidas requieren autenticaciÃ³n. La consulta detallada y la
devoluciÃ³n requieren `admin` o `support`.

## Ejemplos de uso

### Crear un usuario

```json
{
	"name": "Ana GarcÃ­a",
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

### Crear un prÃ©stamo

DespuÃ©s de crear el usuario y el dispositivo, utiliza sus IDs:

```json
{
	"user_id": 1,
	"device_id": 1
}
```

TambiÃ©n puedes probar el flujo desde Swagger UI o con `curl`:

```powershell
curl.exe -X POST http://127.0.0.1:8000/loans/ -H "Content-Type: application/json" -d "{\"user_id\":1,\"device_id\":1}"
curl.exe -X PATCH http://127.0.0.1:8000/loans/1/return
```

## Estructura principal

```text
app/
â”œâ”€â”€ main.py                         # ConfiguraciÃ³n y registro de routers
â”œâ”€â”€ database.py                     # Motor, sesiones y creaciÃ³n de tablas
â”œâ”€â”€ models/                         # Modelos SQLAlchemy
â”‚   â”œâ”€â”€ user_model.py
â”‚   â”œâ”€â”€ device_model.py
â”‚   â””â”€â”€ loan_model.py
â”œâ”€â”€ schemas/                        # ValidaciÃ³n Pydantic
â”œâ”€â”€ routes/                         # Endpoints de la API
â”‚   â”œâ”€â”€ user_routes.py
â”‚   â”œâ”€â”€ device_routes.py
â”‚   â””â”€â”€ loan_routes.py
â””â”€â”€ services/                       # LÃ³gica de negocio
		â”œâ”€â”€ user_service.py
		â”œâ”€â”€ device_service.py
		â””â”€â”€ loan_service.py
alembic/
â””â”€â”€ versions/                       # Historial de migraciones
```

## Respuestas y errores frecuentes

- `200`: operaciÃ³n exitosa.
- `201`: usuario, dispositivo o prÃ©stamo creado.
- `204`: dispositivo eliminado correctamente.
- `400`: nÃºmero de serie duplicado.
- `404`: recurso, usuario o dispositivo no encontrado.
- `409`: dispositivo no disponible, prÃ©stamo ya devuelto o dispositivo con prÃ©stamos asociados.
- `422`: datos enviados no vÃ¡lidos segÃºn los esquemas Pydantic.
- `401`: falta autenticaciÃ³n o el JWT no es vÃ¡lido.
- `403`: el usuario autenticado no tiene permisos suficientes.
- `429`: se superÃ³ el lÃ­mite de solicitudes.

Las contraseÃ±as se almacenan Ãºnicamente como hashes bcrypt mediante Passlib.
Nunca se guarda ni se devuelve la contraseÃ±a original.

## Evidencias

Agrega aquÃ­ las capturas o evidencias reales de Swagger, login, rutas
protegidas, CORS, headers y rate limiting cuando estÃ©n disponibles. No se
incluyen capturas inventadas en el repositorio.

