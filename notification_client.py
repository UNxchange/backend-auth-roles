# notification_client.py
"""
Cliente para comunicarse con el microservicio de notificaciones vía GraphQL
Este archivo debe ser agregado al microservicio de autenticación (backend-auth-roles)
"""

import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class AuthNotificationClient:
    def __init__(self, base_url: str = "http://backend-notifications:8001"):
        self.base_url = base_url
        self.graphql_url = f"{base_url}/api/v1/notification/graphql"
    
    def create_user_with_welcome(self, user_id: int, user_name: str, user_email: str, user_role: str = "estudiante") -> Optional[dict]:
        """
        Crea una notificación y envía correo de bienvenida usando GraphQL
        
        Args:
            user_id: ID real del usuario creado
            user_name: Nombre del usuario creado
            user_email: Email del usuario creado
            user_role: Rol del usuario (estudiante, profesional, administrador)
            
        Returns:
            Respuesta del microservicio de notificaciones o None si hay error
        """
        
        # Mutación GraphQL para crear usuario con bienvenida
        mutation = """
        mutation CreateUserWithWelcome($input: UserInput!) {
            createUserWithWelcome(input: $input) {
                user {
                    id
                    name
                    email
                    role
                }
                welcomeEmail {
                    success
                    message
                    timestamp
                }
                totalUsers
            }
        }
        """
        
        variables = {
            "input": {
                "id": user_id,  # Pasar el ID real del usuario
                "name": user_name,
                "email": user_email,
                "role": user_role.upper()  # ESTUDIANTE, PROFESIONAL, ADMINISTRADOR
            }
        }
        
        payload = {
            "query": mutation,
            "variables": variables
        }
        
        try:
            logger.info(f"Enviando notificación GraphQL para usuario ID {user_id}: {user_email}")
            
            response = requests.post(
                self.graphql_url,
                json=payload,
                timeout=30,
                headers={"Content-Type": "application/json"}
            )
            
            response.raise_for_status()
            result = response.json()
            
            # Verificar si hubo errores en GraphQL
            if "errors" in result:
                logger.error(f"Errores GraphQL al notificar {user_email}: {result['errors']}")
                return None
            
            logger.info(f"Notificación de bienvenida enviada exitosamente para usuario ID {user_id}")
            return result.get("data", {}).get("createUserWithWelcome")
            
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
def send_welcome_email(user_id: int, user_name: str, user_email: str, user_role: str = "estudiante") -> bool:
    """
    Envía un correo de bienvenida a un usuario recién creado usando GraphQL
    
    Args:
        user_id: ID real del usuario
        user_name: Nombre del usuario
        user_email: Email del usuario
        user_role: Rol del usuario (estudiante, profesional, administrador)
        
    Returns:
        True si se envió exitosamente, False en caso contrario
    """
    result = auth_notification_client.create_user_with_welcome(user_id, user_name, user_email, user_role)
    if result and "welcomeEmail" in result:
        return result["welcomeEmail"].get("success", False)
    return False

# Función asíncrona para no bloquear el registro
def send_welcome_email_async(user_id: int, user_name: str, user_email: str, user_role: str = "estudiante") -> None:
    """
    Versión asíncrona que no bloquea el proceso de registro
    Úsala si no quieres que el registro falle por problemas de notificación
    """
    import threading
    
    def _send_notification():
        try:
            send_welcome_email(user_id, user_name, user_email, user_role)
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
