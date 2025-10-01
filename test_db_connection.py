#!/usr/bin/env python3
"""
Script de diagnóstico para probar la conexión a la base de datos PostgreSQL
"""
import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_database_connection():
    """Prueba la conexión a la base de datos con diferentes métodos"""
    
    database_url = os.getenv('DATABASE_URL')
    print(f"🔍 DATABASE_URL cargada: {database_url}")
    print()
    
    if not database_url:
        print("❌ No se encontró DATABASE_URL en las variables de entorno")
        return
    
    # Parsear la URL de la base de datos
    parsed = urlparse(database_url)
    print("📋 Detalles de conexión:")
    print(f"   - Host: {parsed.hostname}")
    print(f"   - Puerto: {parsed.port}")
    print(f"   - Usuario: {parsed.username}")
    print(f"   - Base de datos: {parsed.path[1:]}")  # Remover el '/' inicial
    print(f"   - Password: {'*' * len(parsed.password) if parsed.password else 'No especificada'}")
    print()
    
    # Test 1: Conexión básica
    print("🧪 Test 1: Conexión básica sin SSL")
    try:
        conn = psycopg2.connect(database_url)
        print("✅ Conexión exitosa!")
        
        # Probar una consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 Versión de PostgreSQL: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión: {e}")
        print()
    
    # Test 2: Conexión con SSL requerido
    print("🧪 Test 2: Conexión con SSL requerido")
    try:
        ssl_url = database_url + "?sslmode=require"
        conn = psycopg2.connect(ssl_url)
        print("✅ Conexión con SSL exitosa!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 Versión de PostgreSQL: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión con SSL: {e}")
        print()
    
    # Test 3: Conexión con SSL preferido
    print("🧪 Test 3: Conexión con SSL preferido")
    try:
        ssl_url = database_url + "?sslmode=prefer"
        conn = psycopg2.connect(ssl_url)
        print("✅ Conexión con SSL preferido exitosa!")
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"📊 Versión de PostgreSQL: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.OperationalError as e:
        print(f"❌ Error de conexión con SSL preferido: {e}")
        print()
    
    # Test 4: Diagnóstico de red
    print("🧪 Test 4: Diagnóstico de conectividad de red")
    import socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((parsed.hostname, parsed.port))
        if result == 0:
            print("✅ El host y puerto son accesibles")
        else:
            print(f"❌ No se puede conectar al host {parsed.hostname}:{parsed.port}")
        sock.close()
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
    
    print()
    print("🔍 Posibles causas del problema:")
    print("1. ❌ Credenciales incorrectas o expiradas")
    print("2. ❌ Tu IP no está autorizada en el security group de AWS RDS")
    print("3. ❌ El servidor RDS requiere SSL")
    print("4. ❌ El servidor RDS está fuera de línea o no existe")
    print("5. ❌ Problemas de firewall o conectividad de red")
    
    return False

def get_public_ip():
    """Obtiene la IP pública actual"""
    try:
        import requests
        response = requests.get('https://httpbin.org/ip', timeout=10)
        ip_info = response.json()
        return ip_info.get('origin', 'No disponible')
    except Exception as e:
        return f"Error obteniendo IP: {e}"

if __name__ == "__main__":
    print("🔧 Diagnóstico de Conexión a Base de Datos PostgreSQL")
    print("=" * 60)
    print()
    
    # Mostrar IP pública
    public_ip = get_public_ip()
    print(f"🌐 Tu IP pública actual: {public_ip}")
    print()
    
    # Ejecutar pruebas
    success = test_database_connection()
    
    if not success:
        print()
        print("💡 Sugerencias para solucionar:")
        print("1. Verificar que las credenciales sean correctas")
        print("2. Autorizar tu IP en AWS RDS Security Groups")
        print("3. Probar con sslmode=require en la URL de conexión")
        print("4. Contactar al administrador de la base de datos")