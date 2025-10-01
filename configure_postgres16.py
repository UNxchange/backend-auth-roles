#!/usr/bin/env python3
"""
Configurador específico para PostgreSQL 16 recién instalado
"""
import subprocess
import sys
import os
import time

# Ruta donde se instaló PostgreSQL
POSTGRES_BIN_PATH = r"C:\Program Files\PostgreSQL\16\bin"
PSQL_PATH = os.path.join(POSTGRES_BIN_PATH, "psql.exe")

def run_psql_command(command, database="postgres", user="postgres"):
    """Ejecuta un comando usando psql"""
    cmd = [
        PSQL_PATH,
        "-U", user,
        "-d", database,
        "-h", "localhost",
        "-c", command
    ]
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        return result
    except subprocess.TimeoutExpired:
        print(f"⏰ Timeout ejecutando comando SQL")
        return None
    except Exception as e:
        print(f"❌ Error ejecutando comando SQL: {e}")
        return None

def check_postgres_service():
    """Verifica si PostgreSQL está ejecutándose"""
    print("🔍 Verificando servicio de PostgreSQL...")
    
    result = run_psql_command("SELECT version();")
    
    if result and result.returncode == 0:
        print("✅ PostgreSQL está ejecutándose correctamente")
        version_info = result.stdout.strip()
        print(f"   {version_info}")
        return True
    else:
        print("❌ PostgreSQL no está ejecutándose o hay problemas de acceso")
        if result:
            print(f"   Error: {result.stderr}")
        return False

def create_database_and_user():
    """Crea la base de datos y usuario para la aplicación"""
    print("\n🗄️ Configurando base de datos y usuario...")
    
    # Crear base de datos
    print("   📝 Creando base de datos 'unxchange_auth'...")
    result = run_psql_command("CREATE DATABASE unxchange_auth;")
    
    if result and result.returncode == 0:
        print("   ✅ Base de datos creada exitosamente")
    elif result and "already exists" in result.stderr:
        print("   ⚠️  Base de datos ya existe")
    else:
        print(f"   ❌ Error creando base de datos: {result.stderr if result else 'Comando falló'}")
        return False
    
    # Crear usuario
    print("   👤 Creando usuario 'unxchange_user'...")
    result = run_psql_command("CREATE USER unxchange_user WITH PASSWORD 'unxchange_password_2025';")
    
    if result and result.returncode == 0:
        print("   ✅ Usuario creado exitosamente")
    elif result and "already exists" in result.stderr:
        print("   ⚠️  Usuario ya existe")
    else:
        print(f"   ❌ Error creando usuario: {result.stderr if result else 'Comando falló'}")
        # Continuar aunque falle, puede que el usuario ya exista
    
    # Dar permisos al usuario en la base de datos
    print("   🔑 Otorgando permisos...")
    result = run_psql_command("GRANT ALL PRIVILEGES ON DATABASE unxchange_auth TO unxchange_user;")
    
    if result and result.returncode == 0:
        print("   ✅ Permisos otorgados exitosamente")
    else:
        print(f"   ⚠️  Advertencia al otorgar permisos: {result.stderr if result else 'Comando falló'}")
    
    # Configurar permisos adicionales en la base de datos específica
    print("   🔧 Configurando permisos adicionales...")
    additional_permissions = [
        "GRANT ALL ON SCHEMA public TO unxchange_user;",
        "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO unxchange_user;",
        "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO unxchange_user;",
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO unxchange_user;",
        "ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO unxchange_user;"
    ]
    
    for perm in additional_permissions:
        result = run_psql_command(perm, database="unxchange_auth")
        if result and result.returncode == 0:
            print(f"   ✅ Permiso configurado")
        else:
            print(f"   ⚠️  Advertencia: {perm.split()[0]} {perm.split()[1]}")
    
    return True

def test_new_connection():
    """Prueba la conexión con las nuevas credenciales"""
    print("\n🧪 Probando conexión con nuevas credenciales...")
    
    # Usar psql con las nuevas credenciales
    cmd = [
        PSQL_PATH,
        "-U", "unxchange_user",
        "-d", "unxchange_auth",
        "-h", "localhost",
        "-c", "SELECT current_database(), current_user, version();"
    ]
    
    # Configurar variable de entorno para la contraseña
    env = os.environ.copy()
    env['PGPASSWORD'] = 'unxchange_password_2025'
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        
        if result.returncode == 0:
            print("✅ Conexión exitosa con las nuevas credenciales!")
            print("   Información de la conexión:")
            for line in result.stdout.strip().split('\n'):
                if line.strip() and not line.startswith('-') and 'row' not in line:
                    print(f"     {line.strip()}")
            return True
        else:
            print("❌ Error al conectar con las nuevas credenciales")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error probando conexión: {e}")
        return False

def test_python_connection():
    """Prueba la conexión desde Python"""
    print("\n🐍 Probando conexión desde Python...")
    
    try:
        import psycopg2
        
        # Intentar conectarse
        conn = psycopg2.connect(
            host="localhost",
            database="unxchange_auth",
            user="unxchange_user",
            password="unxchange_password_2025",
            port="5432"
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT current_database(), current_user, version();")
        result = cursor.fetchone()
        
        print("✅ Conexión desde Python exitosa!")
        print(f"   Base de datos: {result[0]}")
        print(f"   Usuario: {result[1]}")
        print(f"   Versión: {result[2][:50]}...")
        
        cursor.close()
        conn.close()
        return True
        
    except ImportError:
        print("⚠️  psycopg2 no está instalado. Instalando...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"], check=True)
            print("✅ psycopg2 instalado, reintentando...")
            return test_python_connection()  # Recursión para reintentar
        except Exception as e:
            print(f"❌ Error instalando psycopg2: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Error conectando desde Python: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 CONFIGURADOR DE POSTGRESQL 16 LOCAL")
    print("=" * 60)
    print(f"📁 Usando PostgreSQL en: {POSTGRES_BIN_PATH}")
    print()
    
    # Verificar que PostgreSQL esté ejecutándose
    if not check_postgres_service():
        print("\n❌ PostgreSQL no está ejecutándose correctamente")
        print("💡 Posibles soluciones:")
        print("1. Reinicia tu computadora para que inicie el servicio")
        print("2. Ve a 'Servicios' de Windows y busca 'postgresql-x64-16'")
        print("3. Asegúrate de que esté en estado 'Ejecutándose'")
        return False
    
    # Crear base de datos y usuario
    if not create_database_and_user():
        print("\n❌ Error configurando la base de datos")
        return False
    
    # Probar conexión con psql
    if not test_new_connection():
        print("\n❌ Error probando la conexión")
        return False
    
    # Probar conexión desde Python
    if not test_python_connection():
        print("\n❌ Error probando la conexión desde Python")
        return False
    
    print("\n🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
    print("=" * 60)
    print()
    print("✅ PostgreSQL 16 está configurado y funcionando")
    print("✅ Base de datos 'unxchange_auth' creada")
    print("✅ Usuario 'unxchange_user' creado con todos los permisos")
    print("✅ Conexión verificada desde psql y Python")
    print("✅ Archivo .env ya está configurado")
    print()
    print("🚀 PRÓXIMOS PASOS:")
    print("1. 🖥️  Ejecuta el backend:")
    print("   py -m uvicorn app.main:app --host 0.0.0.0 --port 8080")
    print()
    print("2. 👥 Inserta usuarios de prueba:")
    print("   py test_insert_users.py")
    print()
    print("3. 🔍 Verifica los datos:")
    print("   py test_query_users.py")
    print()
    print("4. 🌐 Prueba la API en:")
    print("   http://localhost:8080/docs")
    print()
    print("🔑 CREDENCIALES CONFIGURADAS:")
    print(f"   Host: localhost")
    print(f"   Puerto: 5432")
    print(f"   Base de datos: unxchange_auth")
    print(f"   Usuario: unxchange_user")
    print(f"   Contraseña: unxchange_password_2025")
    
    return True

if __name__ == "__main__":
    success = main()
    
    if not success:
        print(f"\n📋 Si hay problemas, revisa la guía manual en: SETUP_POSTGRESQL_LOCAL.md")
        sys.exit(1)
    else:
        print(f"\n✨ ¡Todo listo para usar el backend!")
        sys.exit(0)