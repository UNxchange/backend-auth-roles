# Changelog

Todos los cambios notables de este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-07-13

### Agregado

- **Microservicio de autenticación inicial** para la plataforma UnxChange
- **Sistema de registro de usuarios** (`POST /api/v1/auth/register`)
  - Validación de email único
  - Hash seguro de contraseñas con bcrypt
  - Soporte para roles de usuario (estudiante, profesional, administrador)
  - Integración automática con microservicio de notificaciones
- **Sistema de autenticación JWT** (`POST /api/v1/auth/login`)
  - Login con email y contraseña
  - Generación de tokens JWT con expiración configurable
  - Incluye rol de usuario en el token para autorización
  - Protocolo OAuth2 con Bearer tokens
- **Gestión de usuarios autenticados**
  - Endpoint protegido para obtener todos los usuarios (`GET /api/v1/auth/users/`)
  - Endpoint protegido para obtener usuario por email (`GET /api/v1/auth/user`)
  - Middleware de verificación de tokens JWT
  - Sistema de roles y permisos
- **Integración con microservicio de notificaciones**
  - Cliente HTTP para comunicación con servicio de notificaciones
  - Envío automático de email de bienvenida al registrar usuarios
  - Manejo robusto de errores de notificación (no afecta el registro)
  - Funciones asíncronas para optimizar rendimiento
- **Base de datos PostgreSQL**
  - Modelos SQLAlchemy para usuarios
  - Sistema de roles con enum (estudiante, profesional, administrador)
  - Migración automática de tablas en desarrollo
  - Validación de integridad de datos
- **Arquitectura de microservicio FastAPI**
  - API REST con documentación automática
  - Configuración CORS para integración con frontend
  - Estructura modular con separación de responsabilidades
  - Esquemas Pydantic para validación de datos
- **Sistema de seguridad robusto**
  - Hash de contraseñas con bcrypt y salt
  - Tokens JWT con firma digital
  - Validación de email con Pydantic
  - Protección de endpoints sensibles
- **Configuración de despliegue**
  - Dockerfile para contenarización
  - docker-compose.yml para desarrollo local
  - Procfile para despliegue en Heroku
  - Variables de entorno para configuración segura

### Tecnologías utilizadas

- FastAPI 0.110.0 como framework web principal
- SQLAlchemy 2.0.25 como ORM
- PostgreSQL con psycopg2-binary 2.9.9
- Pydantic 2.5.3 con validación de email
- JWT con python-jose 3.3.0
- Bcrypt 4.1.2 para hash de contraseñas
- OAuth2 con FastAPI Security
- Requests 2.31.0 para comunicación entre microservicios
- Python 3.12+
- Uvicorn para servidor ASGI
- Gunicorn 21.2.0 para producción

### Funcionalidades principales

- ✅ Registro de usuarios con validación
- ✅ Autenticación JWT segura
- ✅ Sistema de roles (estudiante, profesional, administrador)
- ✅ Gestión de usuarios autenticados
- ✅ Integración con microservicio de notificaciones
- ✅ API REST completa con documentación
- ✅ Contenarización con Docker
- ✅ Configuración para múltiples entornos

### Seguridad

- Hash de contraseñas con bcrypt y salt automático
- Tokens JWT con firma HMAC y expiración configurable
- Validación de datos de entrada con Pydantic
- Protección de endpoints con middleware de autenticación
- Variables de entorno para credenciales sensibles
- CORS configurado para producción

### Arquitectura

- **Endpoints**: `/api/v1/auth/` - Rutas de autenticación
- **Modelos**: Sistema de usuarios con roles
- **CRUD**: Operaciones de base de datos optimizadas
- **Core**: Configuración y funciones de seguridad
- **Schemas**: Validación y serialización de datos

### Integración

- **Microservicio de notificaciones**: Envío automático de emails de bienvenida
- **Frontend**: API REST con CORS habilitado
- **Base de datos**: PostgreSQL con migración automática
- **Despliegue**: Docker y Heroku ready

---

## Documentación técnica

### Endpoints disponibles

- `POST /api/v1/auth/register` - Registro de usuarios
- `POST /api/v1/auth/login` - Autenticación y obtención de token
- `GET /api/v1/auth/users/` - Obtener todos los usuarios (requiere auth)
- `GET /api/v1/auth/user` - Obtener usuario por email (requiere auth)
- `GET /` - Health check del servicio

### Modelos de datos

- **User**: Modelo principal con id, name, email, role, hashed_password
- **UserRole**: Enum con roles disponibles (estudiante, profesional, administrador)

### Esquemas Pydantic

- **UserCreate**: Schema para registro de usuarios
- **UserOut**: Schema para respuestas de usuario (sin contraseña)
- **Token**: Schema para respuestas de autenticación
- **TokenData**: Schema para datos del token JWT

---

## Notas de desarrollo

- **Migración de BD**: Actualmente usa `create_all()` para desarrollo, migrar a Alembic en futuras versiones
- **Logs**: Implementar sistema de logging más robusto
- **Testing**: Agregar tests unitarios y de integración
- **Monitoreo**: Implementar métricas de rendimiento y salud del servicio
- **Documentación**: La documentación interactiva está disponible en `/docs`
