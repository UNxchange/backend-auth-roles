# Authentication

Este microservicio es responsable de la autenticación y autorización de los usuarios en el sistema. Proporciona endpoints para el registro, inicio de sesión y gestión de roles.

## Tegnologías

- **Python**: Lenguaje de programación principal.
- **Pydantic**: Para la validación de datos y modelos.
- **FastAPI**: Framework web para construir APIs.
- **SQLAlchemy**: ORM para interactuar con la base de datos.
- **JWT**: Para la generación y validación de tokens de acceso.
- **OAuth2**: Protocolo de autorización utilizado para el inicio de sesión.
- **PostgreSQL**: Base de datos relacional utilizada para almacenar la información de los usuarios.

## Endpoints

- `/register`: Registro de nuevos usuarios.
- `/login`: Inicio de sesión de usuarios.
- `/users/`: Obtiene todos los usuarios.
- `/user/{email}`: Obtiene un usuario por su email.

## Configuración

1. Para configurar el microservicio, es necesario tener un archivo `.env` con las siguientes variables:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY=your_secret_key
```

2. Se debe crear un entorno virtual:

```bash
py -m venv venv
source venv/bin/activate  # En Linux o macOS
venv\Scripts\activate  # En Windows
```

3. Luego, instale las dependencias necesarias:

```bash
pip install -r requirements.txt
```

4. Finalmente, ejecute el servidor:

```bash
uvicorn app.main:app --reload
```

## Probar los Endpoints

Para probar los endpoints, puede utilizar swagger UI disponible en `http://localhost:8000/docs` o utilizar herramientas como Postman o cURL.
