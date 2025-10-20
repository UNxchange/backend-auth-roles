# 📨 Sistema de Message Broker - UnxChange Platform

## 🎯 Descripción General

Este proyecto implementa un **sistema de comunicación asíncrona** entre microservicios utilizando **RabbitMQ** como message broker, permitiendo la comunicación desacoplada entre el servicio de autenticación (`backend-auth-roles`) y el servicio de notificaciones (`backend-notifications`).

## 🏗️ Arquitectura

```
┌─────────────┐         ┌──────────┐         ┌──────────────┐
│  Auth       │ Publish │ RabbitMQ │ Consume │ Notifications│
│  Service    │────────>│  Broker  │────────>│  Service     │
│ (Producer)  │         │          │         │  (Consumer)  │
└─────────────┘         └──────────┘         └──────────────┘
```

### Componentes Principales

1. **RabbitMQ Broker**
   - Exchange: `unxchange_events` (tipo topic)
   - Queue: `notifications_queue` (durable, TTL 24h)
   - Puertos: 5672 (AMQP), 15672 (Management UI)

2. **Producer (backend-auth-roles)**
   - Publica eventos de usuarios
   - Eventos: `user.created`, `user.updated`
   - Mensajes persistentes con prioridades

3. **Consumer (backend-notifications)**
   - Consume eventos de la cola
   - Registra usuarios en BD
   - Envía emails de bienvenida
   - Procesamiento con ACK/NACK

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker Desktop
- Docker Compose
- Puertos libres: 5672, 8000, 8001, 15672

### Iniciar el Sistema

**Windows:**
```powershell
.\start_with_broker.bat
```

**Linux/Mac:**
```bash
chmod +x start_with_broker.sh
./start_with_broker.sh
```

**Manual:**
```bash
docker-compose build
docker-compose up -d
docker-compose logs -f
```

### Verificar que Funciona

1. **RabbitMQ Management UI**: http://localhost:15672
   - Usuario: `unxchange_user`
   - Password: `unxchange_password`

2. **Backend Auth**: http://localhost:8000/docs

3. **Backend Notifications**: http://localhost:8001/docs

4. **Registrar usuario de prueba**:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@unal.edu.co",
    "password": "test123",
    "role": "estudiante"
  }'
```

5. **Ver logs del flujo completo**:
```bash
docker-compose logs -f backend-auth-roles backend-notifications rabbitmq
```

## 📚 Documentación

| Documento | Descripción |
|-----------|-------------|
| **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** | 🚀 Guía paso a paso de despliegue y verificación |
| **[MESSAGE_BROKER_README.md](MESSAGE_BROKER_README.md)** | 📖 Documentación técnica completa del broker |
| **[BROKER_IMPLEMENTATION_SUMMARY.md](BROKER_IMPLEMENTATION_SUMMARY.md)** | 📋 Resumen ejecutivo de la implementación |
| **[ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md)** | 🎨 Diagramas de arquitectura y flujos |
| **[DOCKER_COMPOSE_README.md](DOCKER_COMPOSE_README.md)** | 🐳 Documentación de Docker Compose |

## 📁 Estructura del Proyecto

```
Arqui/
├── docker-compose.yml                          # Orquestación de servicios
├── start_with_broker.bat|.sh                   # Scripts de inicio rápido
├── test_broker.py                              # Tests del broker
│
├── backend-auth-roles/                         # Servicio de autenticación
│   ├── app/
│   │   ├── broker/                            # 🆕 Módulo del producer
│   │   │   ├── __init__.py
│   │   │   └── rabbitmq_client.py            # Cliente RabbitMQ
│   │   └── api/v1/endpoints/
│   │       └── auth.py                        # ✏️ Integrado con broker
│   └── requirements.txt                       # ✏️ + pika
│
├── backend-notifications/                      # Servicio de notificaciones
│   ├── app/
│   │   ├── broker/                            # 🆕 Módulo del consumer
│   │   │   ├── __init__.py
│   │   │   └── rabbitmq_consumer.py          # Consumidor RabbitMQ
│   │   └── main.py                            # ✏️ Inicia consumer
│   └── requirements.txt                       # ✏️ + pika
│
└── Documentación/
    ├── DEPLOYMENT_GUIDE.md                    # 🆕 Guía de despliegue
    ├── MESSAGE_BROKER_README.md               # 🆕 Doc del broker
    ├── BROKER_IMPLEMENTATION_SUMMARY.md       # 🆕 Resumen
    └── ARCHITECTURE_DIAGRAMS.md               # 🆕 Diagramas
```

**Leyenda:**
- 🆕 = Archivo nuevo
- ✏️ = Archivo modificado

## 🔄 Flujo de Operación

### 1. Usuario se Registra
```
Frontend → Backend Auth (POST /register)
```

### 2. Backend Auth Crea Usuario
```
Backend Auth → PostgreSQL (INSERT user)
```

### 3. Backend Auth Publica Evento
```
Backend Auth → RabbitMQ (PUBLISH user.created)
```

### 4. RabbitMQ Almacena Mensaje
```
RabbitMQ → notifications_queue (STORE)
```

### 5. Backend Notifications Consume
```
RabbitMQ → Backend Notifications (DELIVER)
```

### 6. Backend Notifications Procesa
```
Backend Notifications → PostgreSQL (INSERT user)
Backend Notifications → SMTP (SEND email)
Backend Notifications → RabbitMQ (ACK)
```

### 7. RabbitMQ Confirma
```
RabbitMQ → (DELETE message from queue)
```

## 🎯 Casos de Uso

### Evento: Usuario Creado
```json
{
  "event_type": "user_created",
  "user_id": 123,
  "user_name": "Juan Pérez",
  "user_email": "jperez@unal.edu.co",
  "user_role": "ESTUDIANTE",
  "action": "send_welcome_email"
}
```

**Acciones**:
1. ✅ Registrar usuario en BD de notificaciones
2. ✅ Enviar email de bienvenida
3. ✅ Confirmar procesamiento (ACK)

### Evento: Usuario Actualizado
```json
{
  "event_type": "user_updated",
  "user_id": 123,
  "user_email": "jperez@unal.edu.co",
  "changes": {
    "name": "Juan Pablo Pérez",
    "role": "PROFESIONAL"
  }
}
```

**Acciones**:
1. ℹ️ Registrar log del cambio
2. 🔮 (Extensible para notificaciones de cambios)

## 🛠️ Comandos Útiles

### Ver Estado de Servicios
```bash
docker-compose ps
```

### Ver Logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo servicios relacionados con el broker
docker-compose logs -f backend-auth-roles backend-notifications rabbitmq

# Filtrar por palabras clave
docker-compose logs -f | grep "user_created"
```

### Gestión de RabbitMQ
```bash
# Ver colas
docker exec unxchange-rabbitmq rabbitmqctl list_queues

# Ver conexiones
docker exec unxchange-rabbitmq rabbitmqctl list_connections

# Purgar cola (desarrollo)
docker exec unxchange-rabbitmq rabbitmqctl purge_queue notifications_queue
```

### Reiniciar Servicios
```bash
# Reiniciar todo
docker-compose restart

# Reiniciar un servicio
docker-compose restart backend-auth-roles
docker-compose restart backend-notifications
docker-compose restart rabbitmq
```

### Reconstruir Después de Cambios
```bash
docker-compose down
docker-compose build
docker-compose up -d
docker-compose logs -f
```

## 🧪 Testing

### Ejecutar Tests del Broker
```bash
python test_broker.py
```

### Registrar Usuarios de Prueba

**Swagger UI** (Recomendado):
- http://localhost:8000/docs
- Endpoint: `POST /api/v1/auth/register`

**cURL**:
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@unal.edu.co",
    "password": "test123456",
    "role": "estudiante"
  }'
```

**PowerShell**:
```powershell
$body = @{
    name = "Test User"
    email = "test@unal.edu.co"
    password = "test123456"
    role = "estudiante"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/auth/register" `
  -Method Post -ContentType "application/json" -Body $body
```

### Verificar el Flujo

1. **Logs del Producer**:
```bash
docker-compose logs backend-auth-roles | grep "Evento de creación publicado"
```

2. **RabbitMQ Management UI**:
- http://localhost:15672 → Queues → notifications_queue
- Verificar mensajes publicados/consumidos

3. **Logs del Consumer**:
```bash
docker-compose logs backend-notifications | grep "Mensaje recibido\|Correo de bienvenida"
```

## 📊 Monitoreo

### RabbitMQ Dashboard
- **URL**: http://localhost:15672
- **Usuario**: unxchange_user
- **Password**: unxchange_password

**Métricas Importantes**:
- **Ready**: Mensajes esperando procesamiento
- **Unacked**: Mensajes siendo procesados
- **Publish rate**: Mensajes/segundo publicados
- **Consume rate**: Mensajes/segundo consumidos

### Logs en Tiempo Real
```bash
# Terminal 1: Producer
docker-compose logs -f backend-auth-roles | grep "broker\|Evento"

# Terminal 2: Broker
docker-compose logs -f rabbitmq

# Terminal 3: Consumer
docker-compose logs -f backend-notifications | grep "Mensaje\|Notificación"
```

## ⚡ Ventajas del Sistema

| Aspecto | Antes (HTTP Síncrono) | Después (Message Broker) |
|---------|----------------------|--------------------------|
| **Acoplamiento** | ❌ Fuerte | ✅ Débil |
| **Rendimiento** | ❌ Lento (espera email) | ✅ Rápido (asíncrono) |
| **Confiabilidad** | ❌ Fallo en email = fallo en registro | ✅ Procesos independientes |
| **Escalabilidad** | ❌ Difícil | ✅ Horizontal fácil |
| **Tolerancia a Fallos** | ❌ Baja | ✅ Alta (reintentos) |
| **Observabilidad** | ⚠️ Limitada | ✅ Completa (RabbitMQ UI) |

## 🐛 Troubleshooting Rápido

### RabbitMQ no inicia
```bash
docker-compose logs rabbitmq
docker-compose restart rabbitmq
```

### Consumer no recibe mensajes
```bash
docker-compose logs backend-notifications | grep "Consumidor"
docker-compose restart backend-notifications
```

### Mensajes acumulados en cola
```bash
docker exec unxchange-rabbitmq rabbitmqctl list_queues
docker-compose logs backend-notifications | grep "ERROR"
docker-compose restart backend-notifications
```

### Error "Module pika not found"
```bash
docker-compose build backend-auth-roles backend-notifications
docker-compose up -d
```

**Para troubleshooting detallado**: Ver [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) Sección 7

## 🔧 Configuración

### Variables de Entorno

**backend-auth-roles**:
```env
RABBITMQ_URL=amqp://unxchange_user:unxchange_password@rabbitmq:5672/
```

**backend-notifications**:
```env
RABBITMQ_URL=amqp://unxchange_user:unxchange_password@rabbitmq:5672/
SMTP_HOST=smtp.gmail.com
EMAIL_ADDRESS=tu_email@gmail.com
EMAIL_PASSWORD=tu_app_password
```

### Puertos

| Servicio | Puerto | Descripción |
|----------|--------|-------------|
| RabbitMQ AMQP | 5672 | Protocolo de mensajería |
| RabbitMQ Management | 15672 | UI de gestión |
| Backend Auth | 8000 | API de autenticación |
| Backend Notifications | 8001 | API de notificaciones |
| Backend Convocatorias | 8008 | API de convocatorias |
| PostgreSQL | 5432 | Base de datos |
| MongoDB | 27017 | Base de datos |
| Frontend | 3000 | Aplicación web |
| Nginx | 80 | Proxy reverso |

## 🚀 Próximos Pasos

### Extensibilidad

1. **Nuevos Eventos**:
   - `user.deleted` - Notificar eliminación
   - `user.login` - Rastrear accesos
   - `password.reset` - Recuperación de contraseña

2. **Nuevos Consumidores**:
   - Servicio de analytics
   - Servicio de auditoría
   - Servicio de reportes

3. **Mejoras**:
   - Dead Letter Queue (DLQ)
   - Retry policies avanzados
   - Circuit breaker
   - Métricas con Prometheus
   - Dashboards con Grafana

## 📞 Soporte

### Documentación
- 📖 Documentación Técnica: [MESSAGE_BROKER_README.md](MESSAGE_BROKER_README.md)
- 🚀 Guía de Despliegue: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- 🎨 Diagramas: [ARCHITECTURE_DIAGRAMS.md](ARCHITECTURE_DIAGRAMS.md)

### Enlaces Útiles
- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [Pika Python Client](https://pika.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 📝 Changelog

### v1.2.0 (Octubre 2025)
- ✨ Implementación completa del message broker con RabbitMQ
- ✨ Producer en backend-auth-roles
- ✨ Consumer en backend-notifications
- ✨ Procesamiento asíncrono de notificaciones
- 📚 Documentación completa
- 🧪 Scripts de prueba
- 🚀 Scripts de inicio rápido

### v1.1.0 (Anterior)
- ⚡ Comunicación HTTP directa (deprecated)
- ⚡ Notificaciones síncronas

## 📜 Licencia

[Incluir información de licencia del proyecto]

## 👥 Contribuidores

[Incluir información de contribuidores]

---

## ⚡ TL;DR (Inicio Ultra Rápido)

```bash
# 1. Clonar e ir al directorio
cd C:\Users\dcifuentes\Downloads\Arquitectura\Arqui

# 2. Iniciar todo
.\start_with_broker.bat  # Windows
# o
./start_with_broker.sh   # Linux/Mac

# 3. Verificar
# - RabbitMQ UI: http://localhost:15672 (unxchange_user / unxchange_password)
# - Auth API: http://localhost:8000/docs
# - Notifications API: http://localhost:8001/docs

# 4. Probar
docker exec unxchange-auth-service python test_broker_simple.py

# 5. Ver logs
docker-compose logs -f
```

**¡Listo! El sistema está funcionando.** 🎉

---

**Documentación actualizada**: Octubre 2025  
**Versión del sistema**: 1.2.0  
**Tecnologías**: FastAPI, RabbitMQ, PostgreSQL, Docker
