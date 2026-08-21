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

<img width="1112" height="880" alt="image" src="https://github.com/user-attachments/assets/68aba06e-0d5c-4810-84c3-4e53be818e31" />


### GET /users

Se realiza una petición GET para consultar todos los usuarios registrados.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/a2cf4a88-a3f7-4929-b48c-5ba7cc16b048" />





### GET /users?role=admin

Se utiliza un Query Parameter para filtrar los usuarios según su rol.

<img width="1919" height="1076" alt="image" src="https://github.com/user-attachments/assets/34503f2c-4499-4198-b693-594e506df9bd" />

### GET /users?is_active=true

Se utiliza un Query Parameter para filtrar los usuarios según su estado activo o inactivo.

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/e9808c66-1848-4dc2-9104-03577d92288a" />


### POST /users

Se realiza una petición POST para registrar un nuevo usuario.

<img width="921" height="493" alt="image" src="https://github.com/user-attachments/assets/78a8485d-3360-4487-8ab0-bf15af49f039" />


### Validación de datos

La API valida los datos enviados y devuelve un error cuando la información no cumple con las condiciones establecidas.
<img width="921" height="636" alt="image" src="https://github.com/user-attachments/assets/75878807-fb0d-483c-a37e-50a8cef5b657" />


### Cabeceras HTTP

La API devuelve las siguientes cabeceras personalizadas:

- `X-App-Name: device_systems`
- `X-API-Version: 1.0`

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/9e0b3ac7-63ea-452d-8443-319afdd11dbf" />

## Conclusión

FastAPI permite construir APIs REST de manera sencilla y organizada, utilizando métodos HTTP, parámetros de ruta, parámetros de consulta, validación de datos, modelos de respuesta y documentación automática mediante Swagger UI.
