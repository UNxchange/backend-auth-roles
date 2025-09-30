# app/db/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Crea el motor de la base de datos usando la URL del archivo de configuración
print("DATABASE_URL:", settings.DATABASE_URL)  # Para depuración, puedes eliminarlo después

# Para SQLite, necesitamos agregar check_same_thread=False, para PostgreSQL no
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # PostgreSQL y otras bases de datos
    engine = create_engine(settings.DATABASE_URL)

# Crea una fábrica de sesiones (SessionLocal) que se usará para crear nuevas sesiones de DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es una clase base para nuestros modelos ORM. Heredarán de ella.
Base = declarative_base()

# Función de dependencia para obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()