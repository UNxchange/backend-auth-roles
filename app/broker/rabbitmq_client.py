# app/broker/rabbitmq_client.py
"""
Cliente RabbitMQ para publicar mensajes a la cola de notificaciones
Productor de eventos del servicio de autenticación
"""

import json
import logging
from typing import Optional, Dict, Any
import pika
from pika.exceptions import AMQPConnectionError, AMQPChannelError
import os

logger = logging.getLogger(__name__)


class MessageBroker:
    """
    Cliente para publicar mensajes en RabbitMQ
    """
    
    def __init__(self, rabbitmq_url: str = None):
        """
        Inicializa el cliente de RabbitMQ
        
        Args:
            rabbitmq_url: URL de conexión a RabbitMQ (amqp://user:pass@host:port/)
        """
        self.rabbitmq_url = rabbitmq_url or os.getenv(
            "RABBITMQ_URL", 
            "amqp://unxchange_user:unxchange_password@localhost:5672/"
        )
        self.connection = None
        self.channel = None
        self.exchange_name = "unxchange_events"
        self._connect()
    
    def _connect(self):
        """Establece conexión con RabbitMQ"""
        try:
            # Configurar parámetros de conexión
            parameters = pika.URLParameters(self.rabbitmq_url)
            parameters.heartbeat = 600
            parameters.blocked_connection_timeout = 300
            
            # Crear conexión
            self.connection = pika.BlockingConnection(parameters)
            self.channel = self.connection.channel()
            
            # Declarar exchange tipo topic para enrutamiento flexible
            self.channel.exchange_declare(
                exchange=self.exchange_name,
                exchange_type='topic',
                durable=True
            )
            
            # Declarar cola de notificaciones
            self.channel.queue_declare(
                queue='notifications_queue',
                durable=True,
                arguments={'x-message-ttl': 86400000}  # TTL de 24 horas
            )
            
            # Bind de la cola al exchange con routing key para notificaciones
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue='notifications_queue',
                routing_key='user.#'  # Todos los eventos de usuarios
            )
            
            logger.info(f"✅ Conectado a RabbitMQ: {self.rabbitmq_url}")
            
        except AMQPConnectionError as e:
            logger.error(f"❌ Error conectando a RabbitMQ: {e}")
            self.connection = None
            self.channel = None
    
    def publish_message(
        self, 
        routing_key: str, 
        message: Dict[str, Any],
        priority: int = 5
    ) -> bool:
        """
        Publica un mensaje en RabbitMQ
        
        Args:
            routing_key: Clave de enrutamiento (ej: 'user.created', 'user.updated')
            message: Diccionario con el contenido del mensaje
            priority: Prioridad del mensaje (0-10, default 5)
            
        Returns:
            True si el mensaje se publicó correctamente, False en caso contrario
        """
        try:
            # Reconectar si la conexión está cerrada
            if not self.connection or self.connection.is_closed:
                logger.warning("Reconectando a RabbitMQ...")
                self._connect()
            
            if not self.channel:
                logger.error("No hay canal disponible para publicar")
                return False
            
            # Serializar mensaje a JSON
            message_body = json.dumps(message, ensure_ascii=False, default=str)
            
            # Publicar mensaje
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Mensaje persistente
                    priority=priority,
                    content_type='application/json',
                    content_encoding='utf-8'
                )
            )
            
            logger.info(f"✅ Mensaje publicado con routing_key='{routing_key}': {message}")
            return True
            
        except (AMQPConnectionError, AMQPChannelError) as e:
            logger.error(f"❌ Error publicando mensaje: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Error inesperado publicando mensaje: {e}")
            return False
    
    def publish_user_created(
        self,
        user_id: int,
        user_name: str,
        user_email: str,
        user_role: str
    ) -> bool:
        """
        Publica un evento de usuario creado
        
        Args:
            user_id: ID del usuario creado
            user_name: Nombre del usuario
            user_email: Email del usuario
            user_role: Rol del usuario
            
        Returns:
            True si el evento se publicó correctamente
        """
        message = {
            "event_type": "user_created",
            "user_id": user_id,
            "user_name": user_name,
            "user_email": user_email,
            "user_role": user_role.upper(),
            "action": "send_welcome_email"
        }
        
        return self.publish_message(
            routing_key="user.created",
            message=message,
            priority=8  # Alta prioridad para nuevos usuarios
        )
    
    def publish_user_updated(
        self,
        user_id: int,
        user_email: str,
        changes: Dict[str, Any]
    ) -> bool:
        """
        Publica un evento de usuario actualizado
        
        Args:
            user_id: ID del usuario
            user_email: Email del usuario
            changes: Diccionario con los cambios realizados
            
        Returns:
            True si el evento se publicó correctamente
        """
        message = {
            "event_type": "user_updated",
            "user_id": user_id,
            "user_email": user_email,
            "changes": changes
        }
        
        return self.publish_message(
            routing_key="user.updated",
            message=message,
            priority=5
        )
    
    def close(self):
        """Cierra la conexión con RabbitMQ"""
        try:
            if self.channel and not self.channel.is_closed:
                self.channel.close()
            if self.connection and not self.connection.is_closed:
                self.connection.close()
            logger.info("✅ Conexión con RabbitMQ cerrada")
        except Exception as e:
            logger.error(f"Error cerrando conexión: {e}")
    
    def __del__(self):
        """Destructor para cerrar la conexión automáticamente"""
        self.close()


# Instancia global del broker
_message_broker: Optional[MessageBroker] = None


def get_message_broker() -> MessageBroker:
    """
    Obtiene o crea la instancia global del message broker
    
    Returns:
        Instancia del MessageBroker
    """
    global _message_broker
    
    if _message_broker is None:
        _message_broker = MessageBroker()
    
    return _message_broker
