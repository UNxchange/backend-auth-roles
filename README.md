# UnxChange - Servicio de Autenticación

Este microservicio es responsable de la autenticación y autorización de los usuarios en el sistema UnxChange. Proporciona endpoints para el registro, inicio de sesión y gestión de roles de usuarios.

## 🏗️ Tecnologías

- **Python 3.13+**: Lenguaje de programación principal
- **FastAPI**: Framework web moderno para construir APIs REST
- **SQLAlchemy**: ORM para interactuar con la base de datos
- **Pydantic**: Validación de datos y modelos
- **JWT (JSON Web Tokens)**: Para la generación y validación de tokens de acceso
- **OAuth2**: Protocolo de autorización utilizado para el inicio de sesión
- **PostgreSQL**: Base de datos relacional para almacenar información de usuarios
- **Bcrypt**: Hash seguro de contraseñas
- **Uvicorn**: Servidor ASGI para FastAPI
- **Prometheus**: Métricas y monitoreo

## 🚀 Inicio Rápido

### Opción 1: Configuración Automática (Recomendada)

```bash
# 1. Clonar el repositorio y navegar al directorio
cd backend-auth-roles

# 2. Instalar dependencias de Python
pip install -r requirements.txt

# 3. Ejecutar configurador automático de base de datos
python setup_database.py
```

El script `setup_database.py` se encargará de:
- ✅ Verificar si PostgreSQL está instalado
- ✅ Configurar la base de datos automáticamente
- ✅ Crear usuario y permisos necesarios
- ✅ Generar tablas de la aplicación
- ✅ Poblar con usuarios de prueba
- ✅ Configurar archivo `.env`

### Opción 2: Configuración Manual

Si prefieres configurar manualmente o el script automático presenta problemas, sigue la [Guía de Configuración Manual](#-configuración-manual-detallada).

## 🗄️ Configuración de Base de Datos

### Instalación de PostgreSQL

#### Windows (Recomendado: winget)
```bash
winget install PostgreSQL.PostgreSQL.16
```

#### Descarga Manual
1. Ve a: https://www.postgresql.org/download/windows/
2. Descarga PostgreSQL 15 o superior
3. Durante la instalación:
   - **⚠️ IMPORTANTE**: Recuerda la contraseña del usuario `postgres`
   - Puerto: `5432` (por defecto)
   - Marca la opción de iniciar el servicio automáticamente

#### Verificación de Instalación
```bash
psql --version
```

### Configuración de Base de Datos del Proyecto

Una vez instalado PostgreSQL, el script `setup_database.py` creará:

```sql
-- Base de datos
CREATE DATABASE unxchange_auth;

-- Usuario específico para la aplicación
CREATE USER unxchange_user WITH PASSWORD 'unxchange_password_2025';

-- Permisos completos
GRANT ALL PRIVILEGES ON DATABASE unxchange_auth TO unxchange_user;
```

### Estructura de la Base de Datos

#### Tabla `users`
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'estudiante'
);
```

#### Roles Disponibles
- `estudiante`: Usuario estudiante
- `profesional`: Usuario profesional  
- `administrador`: Usuario administrador del sistema

### Archivo `.env`

El archivo `.env` debe contener:
```env
# Configuración de PostgreSQL Local
DATABASE_URL=postgresql://unxchange_user:unxchange_password_2025@localhost:5432/unxchange_auth

# Clave secreta para JWT (cambiar en producción)
SECRET_KEY=your-super-secret-key-change-this-in-production-unxchange-2025

# Configuración adicional
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

## 👥 Usuarios de Prueba

El sistema se configura automáticamente con 5 usuarios de prueba:

| Email | Contraseña | Rol | Nombre |
|-------|------------|-----|--------|
| ana.garcia@unxchange.com | ana123456 | estudiante | Ana García |
| carlos.rodriguez@unxchange.com | carlos123456 | profesional | Carlos Rodríguez |
| maria.lopez@unxchange.com | maria123456 | administrador | María López |
| diego.martinez@unxchange.com | diego123456 | estudiante | Diego Martínez |
| sofia.hernandez@unxchange.com | sofia123456 | profesional | Sofia Hernández |

## 🖥️ Ejecución del Servidor

### Desarrollo
```bash
# Ejecutar servidor de desarrollo
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### Producción
```bash
# Ejecutar servidor de producción
gunicorn app.main:app -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
```

### Docker
```bash
# Construir imagen
docker build -t unxchange-auth .

# Ejecutar contenedor
docker run -p 8080:8000 unxchange-auth

# Con docker-compose (incluye Prometheus y Grafana)
docker-compose up
```

## 🌐 Endpoints de la API

### Base URL
```
http://localhost:8080
```

### Endpoints de Autenticación

#### `POST /api/v1/auth/register`
Registro de nuevos usuarios
```json
{
  "name": "Nuevo Usuario",
  "email": "usuario@ejemplo.com",
  "password": "contraseña123",
  "role": "estudiante"
}
```

#### `POST /api/v1/auth/login`
Inicio de sesión (OAuth2)
```bash
# Content-Type: application/x-www-form-urlencoded
username=ana.garcia@unxchange.com&password=ana123456
```

#### `GET /api/v1/auth/users/`
Obtener todos los usuarios (requiere autenticación)

#### `GET /api/v1/auth/user/{email}`
Obtener usuario específico por email (requiere autenticación)

### Endpoints del Sistema

#### `GET /`
Health check del servicio
```json
{
  "status": "ok",
  "service": "unxchange-auth-service"
}
```

#### `GET /docs`
Documentación interactiva de la API (Swagger UI)

#### `GET /redoc`
Documentación alternativa (ReDoc)

#### `GET /metrics`
Métricas de Prometheus para monitoreo

## 🧪 Pruebas y Verificación

### Scripts de Prueba Incluidos

#### Insertar Usuarios de Prueba
```bash
python test_insert_users.py
```

#### Consultar y Verificar Datos
```bash
python test_query_users.py
```

#### Verificar Conexión a Base de Datos
```bash
python test_db_connection.py
```

### Pruebas con cURL

#### Login
```bash
curl -X POST "http://localhost:8080/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=ana.garcia@unxchange.com&password=ana123456"
```

#### Registro
```bash
curl -X POST "http://localhost:8080/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Usuario Prueba",
    "email": "prueba@test.com",
    "password": "password123",
    "role": "estudiante"
  }'
```

## 🔧 Configuración Manual Detallada

### 1. Instalar PostgreSQL

Sigue las instrucciones de instalación según tu sistema operativo.

### 2. Configurar Base de Datos Manualmente

```sql
-- Conectarse como postgres
psql -U postgres

-- Crear base de datos
CREATE DATABASE unxchange_auth;

-- Crear usuario
CREATE USER unxchange_user WITH PASSWORD 'unxchange_password_2025';

-- Otorgar permisos
GRANT ALL PRIVILEGES ON DATABASE unxchange_auth TO unxchange_user;

-- Conectarse a la base de datos específica
\c unxchange_auth

-- Configurar permisos adicionales
GRANT ALL ON SCHEMA public TO unxchange_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO unxchange_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO unxchange_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO unxchange_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO unxchange_user;

-- Salir
\q
```

### 3. Configurar Entorno Python

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` con la configuración mostrada anteriormente.

### 5. Inicializar Base de Datos

```bash
# Ejecutar backend para crear tablas
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080

# En otra terminal, insertar datos de prueba
python test_insert_users.py
```

## 🛠️ Solución de Problemas

### PostgreSQL no se encuentra
```bash
# Verificar instalación
psql --version

# Verificar servicio (Windows)
Get-Service *postgres*

# Iniciar servicio manualmente
net start postgresql-x64-16
```

### Error de autenticación
- Verifica que la contraseña del usuario `postgres` sea correcta
- Asegúrate de que las credenciales en `.env` coincidan con la configuración

### Error de conexión
- Verifica que PostgreSQL esté ejecutándose en puerto 5432
- Comprueba que el firewall no esté bloqueando la conexión
- Asegúrate de que la base de datos `unxchange_auth` exista

### Error de permisos
```sql
-- Reconectar como postgres y otorgar permisos nuevamente
GRANT ALL PRIVILEGES ON DATABASE unxchange_auth TO unxchange_user;
```

## 🚀 Integración con Frontend

### Variables de Entorno para Frontend

```env
# React/Next.js
REACT_APP_API_BASE_URL=http://localhost:8080
NEXT_PUBLIC_API_BASE_URL=http://localhost:8080

# Vue.js
VUE_APP_API_BASE_URL=http://localhost:8080

# Angular
API_BASE_URL=http://localhost:8080
```

### Ejemplo de Uso en JavaScript

```javascript
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || 'http://localhost:8080';

// Login
const login = async (email, password) => {
  const formData = new FormData();
  formData.append('username', email);
  formData.append('password', password);
  
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/login`, {
    method: 'POST',
    body: formData
  });
  
  return response.json();
};

// Registro
const register = async (userData) => {
  const response = await fetch(`${API_BASE_URL}/api/v1/auth/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData)
  });
  
  return response.json();
};
```

## 📊 Monitoreo y Métricas

### Prometheus
Las métricas están disponibles en `/metrics` y incluyen:
- Número de requests HTTP
- Tiempo de respuesta
- Errores por endpoint
- Usuarios activos

### Grafana
Ejecutar con docker-compose para acceder a dashboards en `http://localhost:3000`

## 🏃‍♂️ Comandos Útiles

```bash
# Verificar configuración completa
python setup_database.py

# Ejecutar todos los tests
python test_insert_users.py && python test_query_users.py

# Verificar logs del servidor
python -m uvicorn app.main:app --log-level debug

# Conectarse directamente a la base de datos
psql -U unxchange_user -d unxchange_auth -h localhost

# Ver tablas en la base de datos
psql -U unxchange_user -d unxchange_auth -h localhost -c "\dt"

# Ver usuarios en la base de datos
psql -U unxchange_user -d unxchange_auth -h localhost -c "SELECT id, name, email, role FROM users;"
```

## 📝 Notas Importantes

- **🔒 Seguridad**: Cambia `SECRET_KEY` en producción
- **🗄️ Backup**: Realiza respaldos regulares de la base de datos
- **🔄 Actualizaciones**: Mantén PostgreSQL y dependencias actualizadas
- **📊 Monitoreo**: Usa las métricas de Prometheus en producción
- **🚀 Escalabilidad**: Considera usar conexión pooling para alta concurrencia

## 📞 Soporte

Si encuentras problemas:

1. Ejecuta `python setup_database.py` para verificación automática
2. Revisa los logs del servidor para errores específicos
3. Verifica que PostgreSQL esté ejecutándose correctamente
4. Consulta la sección de solución de problemas

---

**Desarrollado para UnxChange** 🚀
