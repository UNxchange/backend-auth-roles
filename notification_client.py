# notification_client.py
"""
Cliente para comunicarse con el microservicio de notificaciones
Este archivo debe ser agregado al microservicio de autenticación (backend-auth-roles)
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AuthNotificationClient:
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url
        self.user_created_url = f"{base_url}/api/v1/notification/usuario-creado/"
    
    def notify_user_created(self, user_name: str, user_email: str) -> Optional[dict]:
        """
        Notifica al microservicio de notificaciones que se creó un nuevo usuario
        
        Args:
            user_name: Nombre del usuario creado
            user_email: Email del usuario creado
            
        Returns:
            Respuesta del microservicio de notificaciones o None si hay error
        """
        payload = {
            "name": user_name,
            "email": user_email
        }
        
        try:
            logger.info(f"Notificando creación de usuario: {user_email}")
            
            response = requests.post(
                self.user_created_url,
                json=payload,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            result = response.json()
            
            logger.info(f"Notificación de usuario creado enviada exitosamente para {user_email}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al notificar creación de usuario {user_email}: {e}")
            # No fallar el registro si no se puede enviar el email
            return None
        except Exception as e:
            logger.error(f"Error inesperado al notificar creación de usuario {user_email}: {e}")
            return None

# Instancia global del cliente
auth_notification_client = AuthNotificationClient()

# Función de conveniencia para usar en el endpoint de registro
def send_welcome_email(user_name: str, user_email: str) -> bool:
    """
    Envía un correo de bienvenida a un usuario recién creado
    
    Args:
        user_name: Nombre del usuario
        user_email: Email del usuario
        
    Returns:
        True si se envió exitosamente, False en caso contrario
    """
    result = auth_notification_client.notify_user_created(user_name, user_email)
    return result is not None and result.get("success", False)

# Función asíncrona para no bloquear el registro
def send_welcome_email_async(user_name: str, user_email: str) -> None:
    """
    Versión asíncrona que no bloquea el proceso de registro
    Úsala si no quieres que el registro falle por problemas de notificación
    """
    import threading
    
    def _send_notification():
        try:
            send_welcome_email(user_name, user_email)
        except Exception as e:
            logger.error(f"Error en notificación asíncrona para {user_email}: {e}")
    
    # Ejecutar en un hilo separado
    thread = threading.Thread(target=_send_notification)
    thread.daemon = True
    thread.start()

# Configuración para diferentes entornos
class NotificationConfig:
    DEVELOPMENT = "http://localhost:8002"
    PRODUCTION = "https://notifications.unxchange.com"  # URL de producción
    STAGING = "https://staging-notifications.unxchange.com"  # URL de staging
    
def get_notification_client(environment: str = "development") -> AuthNotificationClient:
    """
    Factory para crear cliente según el entorno
    """
    urls = {
        "development": NotificationConfig.DEVELOPMENT,
        "production": NotificationConfig.PRODUCTION,
        "staging": NotificationConfig.STAGING
    }
    
    base_url = urls.get(environment.lower(), NotificationConfig.DEVELOPMENT)
    return AuthNotificationClient(base_url=base_url)
