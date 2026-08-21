# DEVICE SYSTEMS

## Descripción

Device Systems es una API REST desarrollada con FastAPI para la gestión de usuarios. La aplicación permite consultar, filtrar y registrar usuarios mediante diferentes endpoints HTTP.

## Tecnologías utilizadas

- Python
- FastAPI
- Uvicorn
- Pydantic
- Thunder Client

## Instalación

Instalar las dependencias con:

```bash
pip install fastapi uvicorn
```

## Ejecución

Para iniciar el servidor:

```bash
uvicorn app.main:app --reload
```

La aplicación se ejecuta en:

http://127.0.0.1:8000

La documentación automática se encuentra en:

http://127.0.0.1:8000/docs

## Endpoints

| Método | Endpoint | Función |
|---|---|---|
| GET | `/users` | Lista todos los usuarios |
| GET | `/users/{user_id}` | Busca un usuario por ID |
| GET | `/users?role=admin` | Filtra usuarios por rol |
| GET | `/users?is_active=true` | Filtra usuarios activos |
| POST | `/users` | Registra un nuevo usuario |

## Evidencias

### Swagger UI

Se muestra la documentación automática de la API generada por FastAPI.

**[PEGAR AQUÍ LA CAPTURA DE SWAGGER UI]**

### GET /users

Se realiza una petición GET para consultar todos los usuarios registrados.

**[PEGAR AQUÍ LA CAPTURA DE THUNDER CLIENT DEL GET /users]**

### GET /users/{user_id}

Se utiliza un Path Parameter para consultar un usuario específico mediante su ID.

**[PEGAR AQUÍ LA CAPTURA DEL GET /users/{user_id}]**

### GET /users?role=admin

Se utiliza un Query Parameter para filtrar los usuarios según su rol.

**[PEGAR AQUÍ LA CAPTURA DEL FILTRO POR ROL]**

### GET /users?is_active=true

Se utiliza un Query Parameter para filtrar los usuarios según su estado activo o inactivo.

**[PEGAR AQUÍ LA CAPTURA DEL FILTRO POR ESTADO]**

### POST /users

Se realiza una petición POST para registrar un nuevo usuario.

**[PEGAR AQUÍ LA CAPTURA DEL POST /users]**

### Validación de datos

La API valida los datos enviados y devuelve un error cuando la información no cumple con las condiciones establecidas.

**[PEGAR AQUÍ LA CAPTURA DEL ERROR DE VALIDACIÓN]**

### Cabeceras HTTP

La API devuelve las siguientes cabeceras personalizadas:

- `X-App-Name: device_systems`
- `X-API-Version: 1.0`

**[PEGAR AQUÍ LA CAPTURA DE LOS HEADERS]**

## Conclusión

FastAPI permite construir APIs REST de manera sencilla y organizada, utilizando métodos HTTP, parámetros de ruta, parámetros de consulta, validación de datos, modelos de respuesta y documentación automática mediante Swagger UI.