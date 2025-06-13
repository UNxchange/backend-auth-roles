# app/main.py
from fastapi import FastAPI
from app.api.v1.endpoints import auth
from app.db import models, database
from fastapi.openapi.utils import get_openapi
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware


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

# Configuración CORS para permitir solicitudes desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoint de bienvenida o de health check
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "ok", "service": "unxchange-auth-service"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="UnxChange - Servicio de Autenticación",
        version="0.1.0",
        description="API para gestionar usuarios, roles y autenticación.",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
