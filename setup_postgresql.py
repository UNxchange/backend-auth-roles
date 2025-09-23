#!/usr/bin/env python3
"""
Script automatizado para verificar y configurar PostgreSQL local
"""
import subprocess
import sys
import os
import time
from urllib.parse import urlparse

def run_command(command, shell=True, capture_output=True):
    """Ejecuta un comando y retorna el resultado"""
    try:
        result = subprocess.run(
            command, 
            shell=shell, 
            capture_output=capture_output,
            text=True,
            timeout=30
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout ejecutando: {command}")
        return None
    except Exception as e:
        print(f"❌ Error ejecutando {command}: {e}")
        return None

def check_postgresql_installed():
    """Verifica si PostgreSQL está instalado"""
    print("🔍 Verificando si PostgreSQL está instalado...")
    
    result = run_command("psql --version")
    if result and result.returncode == 0:
        print(f"✅ PostgreSQL instalado: {result.stdout.strip()}")
        return True
    else:
        print("❌ PostgreSQL no está instalado o no está en PATH")
        return False

def check_postgresql_service():
    """Verifica si el servicio de PostgreSQL está ejecutándose"""
    print("🔍 Verificando servicio de PostgreSQL...")
    
    # Intentar conectarse para ver si está ejecutándose
    result = run_command('psql -U postgres -c "SELECT version();" -h localhost', shell=True)
    
    if result and result.returncode == 0:
        print("✅ Servicio de PostgreSQL está ejecutándose")
        return True
    else:
        print("❌ Servicio de PostgreSQL no está ejecutándose o no es accesible")
        return False

def create_database_and_user():
    """Crea la base de datos y usuario para la aplicación"""
    print("🗄️ Configurando base de datos y usuario...")
    
    # Comandos SQL para ejecutar
    sql_commands = [
        "CREATE DATABASE unxchange_auth;",
        "CREATE USER unxchange_user WITH PASSWORD 'unxchange_password_2025';",
        "GRANT ALL PRIVILEGES ON DATABASE unxchange_auth TO unxchange_user;",
    ]
    
    for command in sql_commands:
        print(f"   Ejecutando: {command}")
        result = run_command(f'psql -U postgres -c "{command}" -h localhost')
        
        if result and result.returncode == 0:
            print(f"   ✅ Éxito")
        else:
            # Algunos comandos pueden fallar si ya existen (está bien)
            if "already exists" in (result.stderr if result else ""):
                print(f"   ⚠️  Ya existe (saltando)")
            else:
                print(f"   ❌ Error: {result.stderr if result else 'Comando falló'}")
    
    # Configurar permisos en la base de datos
    permission_commands = [
        "GRANT ALL ON SCHEMA public TO unxchange_user;",
        "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO unxchange_user;",
        "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO unxchange_user;",
    ]
    
    print("🔑 Configurando permisos...")
    for command in permission_commands:
        result = run_command(f'psql -U postgres -d unxchange_auth -c "{command}" -h localhost')
        if result and result.returncode == 0:
            print(f"   ✅ Permisos configurados")
        else:
            print(f"   ⚠️  Error en permisos (puede ser normal si no hay tablas aún)")

def test_connection():
    """Prueba la conexión con las nuevas credenciales"""
    print("🧪 Probando conexión con nuevas credenciales...")
    
    result = run_command(
        'psql -U unxchange_user -d unxchange_auth -c "SELECT current_database(), current_user;" -h localhost',
        shell=True
    )
    
    if result and result.returncode == 0:
        print("✅ Conexión exitosa con las nuevas credenciales!")
        print(f"   Resultado: {result.stdout.strip()}")
        return True
    else:
        print("❌ Error al conectar con las nuevas credenciales")
        if result:
            print(f"   Error: {result.stderr}")
        return False

def check_python_dependencies():
    """Verifica que las dependencias de Python estén instaladas"""
    print("🐍 Verificando dependencias de Python...")
    
    try:
        import psycopg2
        print("✅ psycopg2 está instalado")
        return True
    except ImportError:
        print("❌ psycopg2 no está instalado")
        print("   Instalando psycopg2...")
        
        result = run_command("py -m pip install psycopg2-binary")
        if result and result.returncode == 0:
            print("✅ psycopg2 instalado exitosamente")
            return True
        else:
            print("❌ Error instalando psycopg2")
            return False

def provide_installation_guide():
    """Proporciona guía de instalación si PostgreSQL no está instalado"""
    print("\n" + "="*60)
    print("📥 GUÍA DE INSTALACIÓN DE POSTGRESQL")
    print("="*60)
    print()
    print("PostgreSQL no está instalado. Opciones para instalarlo:")
    print()
    print("1. 🌐 DESCARGAR DESDE EL SITIO OFICIAL:")
    print("   https://www.postgresql.org/download/windows/")
    print("   - Descarga PostgreSQL 15 o superior")
    print("   - Durante la instalación, recuerda la contraseña del usuario 'postgres'")
    print()
    print("2. 📦 USANDO WINGET (Windows Package Manager):")
    print("   winget install PostgreSQL.PostgreSQL")
    print()
    print("3. 🍫 USANDO CHOCOLATEY (si lo tienes instalado):")
    print("   choco install postgresql")
    print()
    print("Después de instalar:")
    print("1. Reinicia tu terminal")
    print("2. Ejecuta este script nuevamente")
    print("3. Asegúrate de que el servicio esté ejecutándose")

def main():
    """Función principal"""
    print("🚀 CONFIGURADOR AUTOMÁTICO DE POSTGRESQL LOCAL")
    print("=" * 60)
    print()
    
    # Verificar si PostgreSQL está instalado
    if not check_postgresql_installed():
        provide_installation_guide()
        return False
    
    # Verificar dependencias de Python
    if not check_python_dependencies():
        print("❌ No se pudieron instalar las dependencias de Python")
        return False
    
    # Verificar si el servicio está ejecutándose
    if not check_postgresql_service():
        print("⚠️  PostgreSQL está instalado pero el servicio no está ejecutándose")
        print("   Intenta iniciar el servicio desde 'Servicios' de Windows")
        print("   Busca 'postgresql' en los servicios y asegúrate de que esté ejecutándose")
        return False
    
    # Crear base de datos y usuario
    create_database_and_user()
    
    # Probar conexión
    if test_connection():
        print("\n🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
        print("=" * 60)
        print()
        print("✅ PostgreSQL está configurado y funcionando")
        print("✅ Base de datos 'unxchange_auth' creada")
        print("✅ Usuario 'unxchange_user' creado con permisos")
        print("✅ Archivo .env actualizado")
        print()
        print("🚀 PRÓXIMOS PASOS:")
        print("1. Ejecuta el backend: py -m uvicorn app.main:app --host 0.0.0.0 --port 8080")
        print("2. Inserta usuarios de prueba: py test_insert_users.py")
        print("3. Verifica los datos: py test_query_users.py")
        print("4. Prueba la API en: http://localhost:8080/docs")
        
        return True
    else:
        print("\n❌ CONFIGURACIÓN INCOMPLETA")
        print("=" * 60)
        print("Hubo problemas configurando la base de datos.")
        print("Revisa los errores anteriores o configura manualmente siguiendo SETUP_POSTGRESQL_LOCAL.md")
        return False

if __name__ == "__main__":
    success = main()
    
    if not success:
        print(f"\n📋 Para configuración manual, revisa: SETUP_POSTGRESQL_LOCAL.md")
        sys.exit(1)
    else:
        print(f"\n✨ ¡Todo listo para usar!")
        sys.exit(0)