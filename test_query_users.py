#!/usr/bin/env python3
"""
Script de prueba para hacer consultas a la base de datos.
Este script verifica los usuarios insertados y prueba diferentes tipos de consultas.
"""

import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import func

# Agregar el directorio raíz al path para importar los módulos de la app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import User, UserRole
from app.core.security import verify_password

def test_user_queries():
    """Realizar diferentes consultas de prueba en la base de datos."""
    
    # Crear sesión de base de datos
    db: Session = SessionLocal()
    
    try:
        print("🔍 CONSULTAS DE PRUEBA")
        print("=" * 50)
        
        # 1. Contar total de usuarios
        total_users = db.query(User).count()
        print(f"📊 Total de usuarios en la base de datos: {total_users}")
        
        # 2. Mostrar todos los usuarios
        print(f"\n👥 LISTA DE TODOS LOS USUARIOS:")
        all_users = db.query(User).all()
        
        if not all_users:
            print("   ⚠️  No hay usuarios en la base de datos")
            return
            
        for user in all_users:
            print(f"   🆔 ID: {user.id}")
            print(f"   📧 Email: {user.email}")
            print(f"   👤 Nombre: {user.name}")
            print(f"   🎭 Rol: {user.role}")
            print(f"   🔒 Hash password: {user.hashed_password[:20]}...")
            print("   " + "-" * 40)
        
        # 3. Consultar usuarios por rol
        print(f"\n🎭 USUARIOS POR ROL:")
        for role in UserRole:
            users_by_role = db.query(User).filter(User.role == role.value).all()
            print(f"   {role.value.upper()}: {len(users_by_role)} usuarios")
            for user in users_by_role:
                print(f"      • {user.name} ({user.email})")
        
        # 4. Buscar usuario específico por email
        print(f"\n🔎 BÚSQUEDA POR EMAIL:")
        test_email = "ana.garcia@unxchange.com"
        user_found = db.query(User).filter(User.email == test_email).first()
        
        if user_found:
            print(f"   ✅ Usuario encontrado: {user_found.name}")
            print(f"      📧 Email: {user_found.email}")
            print(f"      🎭 Rol: {user_found.role}")
        else:
            print(f"   ❌ No se encontró usuario con email: {test_email}")
        
        # 5. Verificar contraseñas (simulando login)
        print(f"\n🔐 PRUEBA DE VERIFICACIÓN DE CONTRASEÑAS:")
        test_credentials = [
            {"email": "ana.garcia@unxchange.com", "password": "ana123456"},
            {"email": "carlos.rodriguez@unxchange.com", "password": "carlos123456"},
            {"email": "maria.lopez@unxchange.com", "password": "wrongpassword"},
        ]
        
        for cred in test_credentials:
            user = db.query(User).filter(User.email == cred["email"]).first()
            if user:
                is_valid = verify_password(cred["password"], user.hashed_password)
                status = "✅ VÁLIDA" if is_valid else "❌ INVÁLIDA"
                print(f"   {cred['email']}: {status}")
            else:
                print(f"   {cred['email']}: ❌ USUARIO NO EXISTE")
        
        # 6. Estadísticas adicionales
        print(f"\n📈 ESTADÍSTICAS:")
        
        # Contar usuarios por dominio de email
        domain_stats = db.query(
            func.substr(User.email, func.position('@' + func.text("'") + " in " + User.email) + 1).label('domain'),
            func.count().label('count')
        ).group_by('domain').all()
        
        print(f"   Usuarios por dominio:")
        for domain, count in domain_stats:
            print(f"      • {domain}: {count} usuarios")
        
        # Usuario con ID más alto (último creado)
        last_user = db.query(User).order_by(User.id.desc()).first()
        if last_user:
            print(f"   Último usuario registrado: {last_user.name} (ID: {last_user.id})")
        
        # 7. Prueba de búsqueda por nombre parcial
        print(f"\n🔍 BÚSQUEDA POR NOMBRE (contiene 'ar'):")
        users_with_ar = db.query(User).filter(User.name.ilike('%ar%')).all()
        for user in users_with_ar:
            print(f"   • {user.name} ({user.email})")
        
    except Exception as e:
        print(f"❌ Error durante las consultas: {e}")
        
    finally:
        db.close()

def test_authentication_simulation():
    """Simular proceso de autenticación completo."""
    
    print(f"\n🚪 SIMULACIÓN DE AUTENTICACIÓN")
    print("=" * 50)
    
    db: Session = SessionLocal()
    
    try:
        # Simular login con diferentes usuarios
        login_attempts = [
            {"email": "ana.garcia@unxchange.com", "password": "ana123456"},
            {"email": "admin@test.com", "password": "admin123"},
            {"email": "maria.lopez@unxchange.com", "password": "maria123456"},
        ]
        
        for attempt in login_attempts:
            print(f"\n🔐 Intento de login: {attempt['email']}")
            
            # Buscar usuario
            user = db.query(User).filter(User.email == attempt['email']).first()
            
            if not user:
                print(f"   ❌ Usuario no encontrado")
                continue
            
            # Verificar contraseña
            if verify_password(attempt['password'], user.hashed_password):
                print(f"   ✅ Autenticación exitosa")
                print(f"   👤 Usuario: {user.name}")
                print(f"   🎭 Rol: {user.role}")
                print(f"   🆔 ID: {user.id}")
            else:
                print(f"   ❌ Contraseña incorrecta")
    
    except Exception as e:
        print(f"❌ Error durante la simulación de autenticación: {e}")
        
    finally:
        db.close()

def main():
    """Función principal del script."""
    print("🔍 Iniciando pruebas de consulta a la base de datos...")
    
    try:
        test_user_queries()
        test_authentication_simulation()
        
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✨ Pruebas de consulta completadas")

if __name__ == "__main__":
    main()