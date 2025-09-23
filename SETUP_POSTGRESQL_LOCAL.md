# ===================================================================
# GUÍA PARA CONFIGURAR POSTGRESQL LOCAL - UNXCHANGE AUTH SERVICE
# ===================================================================

## 1. INSTALACIÓN DE POSTGRESQL

### Opción A: Descargar desde el sitio oficial
1. Ve a: https://www.postgresql.org/download/windows/
2. Descarga PostgreSQL 15 o superior
3. Ejecuta el instalador
4. Durante la instalación:
   - Contraseña para superusuario 'postgres': Elige una contraseña segura
   - Puerto: 5432 (por defecto)
   - Locale: Spanish, Colombia o tu región

### Opción B: Usando Chocolatey (si lo tienes instalado)
```powershell
choco install postgresql
```

### Opción C: Usando winget
```powershell
winget install PostgreSQL.PostgreSQL
```

## 2. VERIFICAR INSTALACIÓN
Después de instalar, abre una nueva terminal PowerShell y ejecuta:
```powershell
psql --version
```

## 3. CREAR BASE DE DATOS Y USUARIO PARA EL PROYECTO

### Conectarse como superusuario
```powershell
psql -U postgres
```

### Ejecutar comandos SQL (uno por línea):
```sql
-- Crear base de datos
CREATE DATABASE unxchange_auth;

-- Crear usuario específico para la aplicación
CREATE USER unxchange_user WITH PASSWORD 'unxchange_password_2025';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON DATABASE unxchange_auth TO unxchange_user;

-- Conectarse a la base de datos creada
\c unxchange_auth

-- Dar permisos sobre el schema público
GRANT ALL ON SCHEMA public TO unxchange_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO unxchange_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO unxchange_user;

-- Salir de psql
\q
```

## 4. CONFIGURACIÓN DEL ARCHIVO .env
Reemplaza el contenido de tu archivo .env con:

```env
DATABASE_URL=postgresql://unxchange_user:unxchange_password_2025@localhost:5432/unxchange_auth
SECRET_KEY=your-super-secret-key-change-this-in-production-unxchange-2025
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

## 5. INICIALIZAR TABLAS Y DATOS DE PRUEBA

Una vez configurado PostgreSQL, ejecuta estos comandos en tu terminal del proyecto:

```powershell
# 1. Ejecutar el backend para crear las tablas
py -m uvicorn app.main:app --host 0.0.0.0 --port 8080

# 2. En otra terminal, insertar usuarios de prueba
py test_insert_users.py

# 3. Verificar que todo funciona
py test_query_users.py
```

## 6. USUARIOS DE PRUEBA QUE SE CREARÁN

| Email | Contraseña | Rol | Nombre |
|-------|------------|-----|--------|
| ana.garcia@unxchange.com | ana123456 | estudiante | Ana García |
| carlos.rodriguez@unxchange.com | carlos123456 | profesional | Carlos Rodríguez |
| maria.lopez@unxchange.com | maria123456 | administrador | María López |
| diego.martinez@unxchange.com | diego123456 | estudiante | Diego Martínez |
| sofia.hernandez@unxchange.com | sofia123456 | profesional | Sofia Hernández |

## 7. ESTRUCTURA DE LA BASE DE DATOS

La tabla principal es `users` con la siguiente estructura:

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'estudiante'
);

CREATE INDEX ix_users_id ON users(id);
CREATE INDEX ix_users_name ON users(name);
CREATE UNIQUE INDEX ix_users_email ON users(email);
```

Roles disponibles:
- `estudiante`: Usuario estudiante
- `profesional`: Usuario profesional
- `administrador`: Usuario administrador

## 8. VERIFICACIÓN FINAL

Para verificar que todo funciona:

1. Backend ejecutándose: http://localhost:8080
2. Documentación API: http://localhost:8080/docs
3. Health check: http://localhost:8080/
4. Usuarios creados correctamente en la DB

## 9. COMANDOS ÚTILES DE POSTGRESQL

```powershell
# Conectarse a la base de datos del proyecto
psql -U unxchange_user -d unxchange_auth -h localhost

# Ver tablas
\dt

# Ver usuarios
SELECT * FROM users;

# Ver estructura de tabla
\d users

# Salir
\q
```

## 10. SOLUCIÓN DE PROBLEMAS

Si tienes problemas:

1. **PostgreSQL no inicia**: 
   - Verifica en Servicios de Windows que "postgresql-x64-15" esté ejecutándose
   - Reinicia el servicio si es necesario

2. **Error de conexión**:
   - Verifica que el puerto 5432 no esté bloqueado
   - Asegúrate de que PostgreSQL esté escuchando en localhost

3. **Error de autenticación**:
   - Verifica usuario y contraseña en .env
   - Asegúrate de haber ejecutado los comandos SQL correctamente

4. **Permisos**:
   - Ejecuta los comandos GRANT como se muestran arriba