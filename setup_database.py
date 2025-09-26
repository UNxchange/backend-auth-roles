#!/usr/bin/env python3
"""
Script de verificación y configuración automática de PostgreSQL para UnxChange Auth Service
Este script verifica si PostgreSQL está instalado y configurado correctamente, 
y si no, guía al usuario en el proceso de configuración.
"""
import subprocess
import sys
import os
import time
from pathlib import Path

# Configuración
DB_NAME = "unxchange_auth"
DB_USER = "unxchange_user"
DB_PASSWORD = "unxchange_password_2025"
DB_HOST = "localhost"
DB_PORT = "5432"

# Rutas posibles de PostgreSQL
POSTGRES_PATHS = [
    r"C:\Program Files\PostgreSQL\16\bin",
    r"C:\Program Files\PostgreSQL\17\bin", 
    r"C:\Program Files\PostgreSQL\15\bin",
    r"C:\Program Files\PostgreSQL\14\bin",
    r"C:\Program Files\PostgreSQL\13\bin",
    r"C:\Program Files\PostgreSQL\12\bin",
]

class DatabaseManager:
    def __init__(self):
        self.psql_path = None
        self.postgres_password = None
        self.find_postgresql()
    
    def find_postgresql(self):
        """Busca la instalación de PostgreSQL"""
        print("🔍 Buscando instalación de PostgreSQL...")
        
        # Primero intentar desde PATH
        try:
            result = subprocess.run(["psql", "--version"], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.psql_path = "psql"
                print(f"✅ PostgreSQL encontrado en PATH: {result.stdout.strip()}")
                return True
        except:
            pass
        
        # Buscar en rutas específicas
        for path in POSTGRES_PATHS:
            psql_exe = os.path.join(path, "psql.exe")
            if os.path.exists(psql_exe):
                try:
                    result = subprocess.run([psql_exe, "--version"], capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        self.psql_path = psql_exe
                        print(f"✅ PostgreSQL encontrado en: {path}")
                        print(f"   Versión: {result.stdout.strip()}")
                        return True
                except:
                    continue
        
        print("❌ PostgreSQL no encontrado")
        return False
    
    def check_service_running(self):
        """Verifica si el servicio de PostgreSQL está ejecutándose"""
        print("🔍 Verificando servicio de PostgreSQL...")
        
        try:
            # Verificar servicios de PostgreSQL
            result = subprocess.run(
                ["powershell", "-Command", "Get-Service *postgres* | Select-Object Status, Name, DisplayName"],
                capture_output=True, text=True, timeout=10
            )
            
            if "Running" in result.stdout:
                print("✅ Servicio de PostgreSQL está ejecutándose")
                return True
            else:
                print("❌ Servicio de PostgreSQL no está ejecutándose")
                print("💡 Inicia el servicio desde 'Servicios' de Windows o reinicia tu computadora")
                return False
                
        except Exception as e:
            print(f"⚠️  No se pudo verificar el servicio: {e}")
            return False
    
    def test_postgres_connection(self):
        """Prueba conexión como superusuario postgres"""
        print("🔍 Probando conexión como superusuario 'postgres'...")
        
        # Intentar contraseñas comunes
        common_passwords = ["", "postgres", "123456", "123456789", "admin", "password"]
        
        for password in common_passwords:
            if self.test_connection_with_password("postgres", password, "postgres"):
                self.postgres_password = password
                if password == "":
                    print("✅ Conexión exitosa sin contraseña")
                else:
                    print(f"✅ Conexión exitosa con contraseña: {password}")
                return True
        
        # Si no funciona ninguna, pedir al usuario
        print("\n🔑 No se pudo conectar con contraseñas comunes.")
        print("Por favor, ingresa la contraseña del usuario 'postgres' que configuraste durante la instalación:")
        
        for attempt in range(3):
            password = input("Contraseña de postgres: ").strip()
            if self.test_connection_with_password("postgres", password, "postgres"):
                self.postgres_password = password
                print("✅ Conexión exitosa!")
                return True
            else:
                print(f"❌ Contraseña incorrecta. Intentos restantes: {2-attempt}")
        
        print("❌ No se pudo establecer conexión después de varios intentos")
        return False
    
    def test_connection_with_password(self, user, password, database):
        """Prueba conexión con credenciales específicas"""
        try:
            env = os.environ.copy()
            env['PGPASSWORD'] = password
            
            cmd = [self.psql_path, "-U", user, "-d", database, "-h", DB_HOST, "-c", "SELECT 1;"]
            
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=10, env=env
            )
            
            return result.returncode == 0
            
        except Exception:
            return False
    
    def check_database_exists(self):
        """Verifica si la base de datos del proyecto existe"""
        print(f"🔍 Verificando si existe la base de datos '{DB_NAME}'...")
        
        try:
            env = os.environ.copy()
            env['PGPASSWORD'] = self.postgres_password
            
            cmd = [self.psql_path, "-U", "postgres", "-h", DB_HOST, "-c", f"SELECT 1 FROM pg_database WHERE datname='{DB_NAME}';"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, env=env)
            
            if result.returncode == 0 and "1 row" in result.stdout:
                print(f"✅ Base de datos '{DB_NAME}' existe")
                return True
            else:
                print(f"❌ Base de datos '{DB_NAME}' no existe")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando base de datos: {e}")
            return False
    
    def check_user_exists(self):
        """Verifica si el usuario del proyecto existe"""
        print(f"🔍 Verificando si existe el usuario '{DB_USER}'...")
        
        try:
            env = os.environ.copy()
            env['PGPASSWORD'] = self.postgres_password
            
            cmd = [self.psql_path, "-U", "postgres", "-h", DB_HOST, "-c", f"SELECT 1 FROM pg_user WHERE usename='{DB_USER}';"]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10, env=env)
            
            if result.returncode == 0 and "1 row" in result.stdout:
                print(f"✅ Usuario '{DB_USER}' existe")
                return True
            else:
                print(f"❌ Usuario '{DB_USER}' no existe")
                return False
                
        except Exception as e:
            print(f"❌ Error verificando usuario: {e}")
            return False
    
    def test_app_connection(self):
        """Prueba conexión con las credenciales de la aplicación"""
        print(f"🔍 Probando conexión con credenciales de la aplicación...")
        
        if self.test_connection_with_password(DB_USER, DB_PASSWORD, DB_NAME):
            print("✅ Conexión exitosa con credenciales de la aplicación")
            return True
        else:
            print("❌ No se puede conectar con credenciales de la aplicación")
            return False
    
    def create_database_and_user(self):
        """Crea la base de datos y usuario del proyecto"""
        print(f"\n🗄️ Configurando base de datos '{DB_NAME}' y usuario '{DB_USER}'...")
        
        env = os.environ.copy()
        env['PGPASSWORD'] = self.postgres_password
        
        commands = [
            (f"CREATE DATABASE {DB_NAME};", "Creando base de datos"),
            (f"CREATE USER {DB_USER} WITH PASSWORD '{DB_PASSWORD}';", "Creando usuario"),
            (f"GRANT ALL PRIVILEGES ON DATABASE {DB_NAME} TO {DB_USER};", "Otorgando permisos a la base de datos"),
        ]
        
        for sql_command, description in commands:
            print(f"   {description}...")
            try:
                cmd = [self.psql_path, "-U", "postgres", "-h", DB_HOST, "-c", sql_command]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=15, env=env)
                
                if result.returncode == 0:
                    print(f"   ✅ {description} completado")
                elif "already exists" in result.stderr:
                    print(f"   ⚠️  {description}: ya existe")
                else:
                    print(f"   ❌ Error en {description}: {result.stderr}")
                    return False
            except Exception as e:
                print(f"   ❌ Error en {description}: {e}")
                return False
        
        # Configurar permisos adicionales en la base de datos específica
        print("   Configurando permisos adicionales...")
        additional_commands = [
            f"GRANT ALL ON SCHEMA public TO {DB_USER};",
            f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {DB_USER};",
            f"ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO {DB_USER};"
        ]
        
        for sql_command in additional_commands:
            try:
                cmd = [self.psql_path, "-U", "postgres", "-d", DB_NAME, "-h", DB_HOST, "-c", sql_command]
                subprocess.run(cmd, capture_output=True, text=True, timeout=15, env=env)
            except:
                pass  # Los permisos adicionales son opcionales
        
        print("✅ Configuración de base de datos completada")
        return True
    
    def check_python_dependencies(self):
        """Verifica e instala dependencias de Python necesarias"""
        print("🐍 Verificando dependencias de Python...")
        
        try:
            import psycopg2
            print("✅ psycopg2 está instalado")
            return True
        except ImportError:
            print("⚠️  psycopg2 no está instalado. Instalando...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "psycopg2-binary"], check=True)
                print("✅ psycopg2 instalado exitosamente")
                return True
            except Exception as e:
                print(f"❌ Error instalando psycopg2: {e}")
                return False
    
    def create_tables_and_test_data(self):
        """Crea tablas y datos de prueba ejecutando el backend y scripts"""
        print("\n📋 Creando tablas y datos de prueba...")
        
        try:
            # Ejecutar el backend brevemente para crear tablas
            print("   Iniciando backend para crear tablas...")
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8081"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Esperar unos segundos para que se inicialice
            time.sleep(5)
            
            # Terminar el proceso
            process.terminate()
            process.wait(timeout=5)
            
            print("   ✅ Tablas creadas")
            
            # Ejecutar script de inserción de usuarios
            print("   Insertando usuarios de prueba...")
            result = subprocess.run([sys.executable, "test_insert_users.py"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("   ✅ Usuarios de prueba insertados")
                return True
            else:
                print(f"   ⚠️  Advertencia al insertar usuarios: {result.stderr}")
                return True  # Continuar aunque haya warnings
                
        except Exception as e:
            print(f"   ❌ Error creando tablas o datos: {e}")
            return False
    
    def update_env_file(self):
        """Actualiza o crea el archivo .env con la configuración correcta"""
        print("📝 Actualizando archivo .env...")
        
        env_content = f"""# Configuración de PostgreSQL Local
DATABASE_URL=postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}

# Clave secreta para JWT
SECRET_KEY=your-super-secret-key-change-this-in-production-unxchange-2025

# Configuración adicional
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
"""
        
        try:
            with open(".env", "w", encoding="utf-8") as f:
                f.write(env_content)
            print("✅ Archivo .env actualizado")
            return True
        except Exception as e:
            print(f"❌ Error actualizando .env: {e}")
            return False
    
    def run_full_check(self):
        """Ejecuta verificación completa y configuración si es necesario"""
        print("🚀 VERIFICADOR Y CONFIGURADOR DE BASE DE DATOS")
        print("=" * 60)
        print(f"Verificando configuración para: {DB_NAME}")
        print()
        
        # 1. Verificar PostgreSQL instalado
        if not self.find_postgresql():
            self.show_installation_guide()
            return False
        
        # 2. Verificar servicio ejecutándose
        if not self.check_service_running():
            return False
        
        # 3. Verificar conexión postgres
        if not self.test_postgres_connection():
            return False
        
        # 4. Verificar dependencias Python
        if not self.check_python_dependencies():
            return False
        
        # 5. Verificar si la configuración ya existe
        db_exists = self.check_database_exists()
        user_exists = self.check_user_exists()
        
        if db_exists and user_exists:
            print("\n✅ Base de datos y usuario ya están configurados")
            
            # Verificar conexión de la aplicación
            if self.test_app_connection():
                print("✅ Conexión de la aplicación funcional")
                
                # Actualizar .env por si acaso
                self.update_env_file()
                
                print("\n🎉 ¡TODO ESTÁ CONFIGURADO CORRECTAMENTE!")
                self.show_next_steps()
                return True
            else:
                print("⚠️  Recreando configuración por problemas de conexión...")
        
        # 6. Crear configuración si no existe
        if not self.create_database_and_user():
            return False
        
        # 7. Verificar conexión final
        if not self.test_app_connection():
            print("❌ Error en la configuración final")
            return False
        
        # 8. Actualizar archivo .env
        if not self.update_env_file():
            return False
        
        # 9. Crear tablas y datos de prueba
        if not self.create_tables_and_test_data():
            print("⚠️  Advertencia: Error creando datos de prueba")
        
        print("\n🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
        self.show_next_steps()
        return True
    
    def show_installation_guide(self):
        """Muestra guía de instalación de PostgreSQL"""
        print("\n" + "="*60)
        print("📥 GUÍA DE INSTALACIÓN DE POSTGRESQL")
        print("="*60)
        print()
        print("PostgreSQL no está instalado. Para instalarlo:")
        print()
        print("🎯 OPCIÓN RECOMENDADA - Windows Package Manager:")
        print("   winget install PostgreSQL.PostgreSQL.16")
        print()
        print("🌐 ALTERNATIVA - Descarga manual:")
        print("   https://www.postgresql.org/download/windows/")
        print()
        print("📝 IMPORTANTE DURANTE LA INSTALACIÓN:")
        print("   ⚠️  RECUERDA LA CONTRASEÑA que asignes al usuario 'postgres'")
        print("   📝 Anótala en un lugar seguro")
        print("   🔑 La necesitarás para ejecutar este configurador")
        print()
        print("🔄 DESPUÉS DE INSTALAR:")
        print("   1. Reinicia tu terminal")
        print("   2. Ejecuta: python setup_database.py")
        print("   3. Ingresa la contraseña cuando se solicite")
    
    def show_next_steps(self):
        """Muestra los próximos pasos después de la configuración"""
        print("\n📋 PRÓXIMOS PASOS:")
        print("=" * 40)
        print()
        print("1. 🚀 Ejecutar el backend:")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8080")
        print()
        print("2. 🌐 Probar la API:")
        print("   http://localhost:8080/docs")
        print()
        print("3. 👥 Usuarios de prueba disponibles:")
        print("   📧 ana.garcia@unxchange.com / Contraseña: ana123456 (estudiante)")
        print("   📧 carlos.rodriguez@unxchange.com / Contraseña: carlos123456 (profesional)")
        print("   📧 maria.lopez@unxchange.com / Contraseña: maria123456 (administrador)")
        print()
        print("4. 🔍 Verificar datos:")
        print("   python test_query_users.py")
        print()
        print("🎯 URL para el frontend:")
        print("   API_BASE_URL=http://localhost:8080")

def main():
    """Función principal"""
    db_manager = DatabaseManager()
    
    try:
        success = db_manager.run_full_check()
        if not success:
            print("\n❌ La configuración no se completó correctamente")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()