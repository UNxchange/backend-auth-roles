# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.db import models, database

# Crea las tablas en la base de datos si no existen
# Esto es útil para el desarrollo, pero para producción se recomienda usar herramientas de migración como Alembic.
try:
    models.Base.metadata.create_all(bind=database.engine)
    print("Tablas de la base de datos creadas (si no existían).")
except Exception as e:
    print(f"Error al crear las tablas de la base de datos: {e}")

# Crea la instancia de la aplicación FastAPI
app = FastAPI(
    title="UnxChange - Servicio de Autenticación",
    description="API para gestionar usuarios, roles y autenticación.",
    version="0.1.0"
)

# Incluye el router de autenticación con un prefijo
# Todas las rutas en `auth.py` ahora comenzarán con /api/v1/auth
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Autenticación"])

# Endpoint de bienvenida o de health check
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok", "service": "unxchange-auth-service"}