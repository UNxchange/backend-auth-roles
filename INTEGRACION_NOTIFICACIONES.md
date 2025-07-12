# Integración con Microservicio de Notificaciones

## Para Microservicio de Autenticación

### Instalación

1. Copiar `notification_client.py` al directorio raíz del proyecto
2. Instalar dependencia adicional:
```bash
pip install requests
```

### Uso en el endpoint de registro

```python
# En app/api/v1/endpoints/auth.py
from notification_client import send_welcome_email_async

@router.post("/register", response_model=schemas.UserOut)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    # ... lógica de registro existente ...
    created_user = crud_user.create_user(db=db, user=user_in)
    
    # Enviar correo de bienvenida (asíncrono)
    try:
        send_welcome_email_async(created_user.name, created_user.email)
    except Exception as e:
        logger.error(f"Error al enviar correo de bienvenida: {e}")
    
    return created_user
```

### Configuración por ambiente

```python
from notification_client import get_notification_client

# Desarrollo
client = get_notification_client("development")  # http://localhost:8002

# Producción
client = get_notification_client("production")  # https://notifications.unxchange.com
```

### Funciones disponibles

- `send_welcome_email(name, email)` - Síncrono
- `send_welcome_email_async(name, email)` - Asíncrono (recomendado)
- `get_notification_client(environment)` - Factory para diferentes entornos

### Logging

El cliente incluye logging automático:
- ✅ Notificaciones enviadas exitosamente
- ❌ Errores de conexión o envío
- ℹ️ Información de debug

### Manejo de errores

- Si el microservicio de notificaciones no está disponible, el registro **NO falla**
- Se loggea el error pero el usuario se crea correctamente
- Usar versión asíncrona para mejor rendimiento
