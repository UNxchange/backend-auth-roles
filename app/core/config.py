# # # app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"
    
##Configuracion local de la base de datos, utilizar para pruebas si se necesita
"""class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432  # Puerto por defecto para PostgreSQL
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"""

settings = Settings()

# app/core/config.py

# from pydantic import PostgresDsn, field_validator
# from pydantic_settings import BaseSettings
# from typing import Optional, Dict, Any

# class Settings(BaseSettings):
#     # --- Configuración de Seguridad para JWT ---
#     SECRET_KEY: str
#     ALGORITHM: str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8 # 8 días de expiración

#     # --- Configuración de la Base de Datos (variables individuales) ---
#     POSTGRES_HOST: str
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_DB: str
#     POSTGRES_PORT: int = 5432

#     # --- URL de la Base de Datos (construida dinámicamente) ---
#     # Esta variable no se leerá directamente del .env, sino que se ensamblará.
#     # Usamos un campo privado con `None` como valor por defecto.
#     DATABASE_URL: Optional[PostgresDsn] = None

#     @field_validator("DATABASE_URL", mode="before")
#     @classmethod
#     def assemble_db_connection(cls, v: Optional[str], values: Any) -> Any:
#         """
#         Ensambla la URL de conexión a la base de datos a partir de las variables individuales.
#         Pydantic ejecutará esta validación para construir el campo DATABASE_URL.
#         """
#         if isinstance(v, str):
#             # Si DATABASE_URL ya está definida en el .env, la usamos directamente.
#             return v
        
#         # Si no, la construimos a partir de las otras variables.
#         # El método `values.data` nos da acceso a los otros campos del modelo.
#         data = values.data
#         return str(PostgresDsn.build(
#             scheme="postgresql",
#             username=data.get("POSTGRES_USER"),
#             password=data.get("POSTGRES_PASSWORD"),
#             host=data.get("POSTGRES_HOST"),
#             port=data.get("POSTGRES_PORT"),
#             path=f"{data.get('POSTGRES_DB') or ''}",
#         ))

#     class Config:
#         # Especifica el archivo del que se leerán las variables de entorno.
#         env_file = ".env"
#         # Permite ignorar mayúsculas y minúsculas en los nombres de las variables.
#         case_sensitive = False
#  # Para depuración, puedes eliminarlo después
# # Creamos una instancia única de la configuración que será importada en otros módulos.
# settings = Settings()