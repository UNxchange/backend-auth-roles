#!/usr/bin/env python3
# test_broker_simple.py
"""
Script de prueba simple para verificar el funcionamiento del message broker
Ejecutar dentro del contenedor: docker exec -it unxchange-auth-service python test_broker_simple.py
"""

from app.broker import get_message_broker
import time

def test_broker_connection():
    """Prueba la conexión al broker"""
    print("=" * 60)
    print("TEST 1: Conexión al Message Broker")
    print("=" * 60)
    
    try:
        broker = get_message_broker()
        print("✅ Conexión establecida exitosamente")
        return True
    except Exception as e:
        print(f"❌ Error conectando al broker: {e}")
        return False

def test_publish_user_created():
    """Prueba la publicación de un evento user.created"""
    print("\n" + "=" * 60)
    print("TEST 2: Publicar evento user.created")
    print("=" * 60)
    
    try:
        broker = get_message_broker()
        
        test_user = {
            "user_id": 9999,
            "user_name": "Usuario Test",
            "user_email": "test@unal.edu.co",
            "user_role": "ESTUDIANTE"
        }
        
        print(f"Publicando evento para usuario: {test_user['user_email']}")
        
        success = broker.publish_user_created(
            user_id=test_user["user_id"],
            user_name=test_user["user_name"],
            user_email=test_user["user_email"],
            user_role=test_user["user_role"]
        )
        
        if success:
            print("✅ Evento publicado exitosamente")
            print(f"   - User ID: {test_user['user_id']}")
            print(f"   - Email: {test_user['user_email']}")
            print(f"   - Role: {test_user['user_role']}")
            return True
        else:
            print("❌ No se pudo publicar el evento")
            return False
            
    except Exception as e:
        print(f"❌ Error publicando evento: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_publish_multiple_events():
    """Prueba la publicación de múltiples eventos"""
    print("\n" + "=" * 60)
    print("TEST 3: Publicar múltiples eventos")
    print("=" * 60)
    
    try:
        broker = get_message_broker()
        users = [
            {"id": 10001, "name": "Ana García", "email": "agarcia@unal.edu.co", "role": "ESTUDIANTE"},
            {"id": 10002, "name": "Carlos López", "email": "clopez@unal.edu.co", "role": "PROFESIONAL"},
            {"id": 10003, "name": "María Rodríguez", "email": "mrodriguez@unal.edu.co", "role": "ADMINISTRADOR"},
        ]
        
        success_count = 0
        
        for i, user in enumerate(users, 1):
            print(f"\nPublicando evento {i}/{len(users)}: {user['email']}")
            success = broker.publish_user_created(
                user_id=user["id"],
                user_name=user["name"],
                user_email=user["email"],
                user_role=user["role"]
            )
            if success:
                success_count += 1
                print(f"  ✅ Publicado correctamente")
            else:
                print(f"  ❌ Error en publicación")
            
            time.sleep(0.5)  # Pequeña pausa entre mensajes
        
        print(f"\n📊 Resultado: {success_count}/{len(users)} eventos publicados exitosamente")
        return success_count == len(users)
    except Exception as e:
        print(f"❌ Error publicando múltiples eventos: {e}")
        return False

def test_publish_user_updated():
    """Prueba la publicación de un evento user.updated"""
    print("\n" + "=" * 60)
    print("TEST 4: Publicar evento user.updated")
    print("=" * 60)
    
    try:
        broker = get_message_broker()
        
        success = broker.publish_user_updated(
            user_id=9999,
            user_email="test@unal.edu.co",
            changes={
                "name": "Usuario Test Actualizado",
                "role": "PROFESIONAL"
            }
        )
        
        if success:
            print("✅ Evento de actualización publicado exitosamente")
            return True
        else:
            print("❌ No se pudo publicar el evento de actualización")
            return False
            
    except Exception as e:
        print(f"❌ Error publicando evento de actualización: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "🚀" * 30)
    print("PRUEBAS DEL MESSAGE BROKER - UnxChange")
    print("Ejecutando desde contenedor: unxchange-auth-service")
    print("🚀" * 30 + "\n")
    
    tests = [
        ("Conexión al Broker", test_broker_connection),
        ("Publicar evento user.created", test_publish_user_created),
        ("Publicar múltiples eventos", test_publish_multiple_events),
        ("Publicar evento user.updated", test_publish_user_updated),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Error ejecutando test '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumen
    print("\n" + "=" * 60)
    print("RESUMEN DE PRUEBAS")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-" * 60)
    print(f"Total: {passed}/{total} pruebas exitosas")
    print("-" * 60)
    
    if passed == total:
        print("\n🎉 ¡Todas las pruebas pasaron exitosamente!")
        print("\n💡 Verifica los logs del consumer para ver los mensajes procesados:")
        print("   docker-compose logs -f backend-notifications | grep 'Mensaje recibido'")
        return 0
    else:
        print(f"\n⚠️ {total - passed} prueba(s) fallaron")
        return 1

if __name__ == "__main__":
    exit(main())
