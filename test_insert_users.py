#!/usr/bin/env python3
"""
Script de prueba para insertar usuarios de prueba en la base de datos.
Este script agrega 5 usuarios con diferentes roles para testing.
"""

import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# Agregar el directorio raíz al path para importar los módulos de la app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.db.database import SessionLocal
from app.db.models import User, UserRole
from app.core.security import get_password_hash

def create_test_users():
    """Crear usuarios de prueba en la base de datos."""
    
    # Lista de usuarios de prueba con diferentes roles
    test_users = [
        {
            "name": "Ana García",
            "email": "ana.garcia@unxchange.com",
            "password": "ana123456",
            "role": UserRole.estudiante.value
        },
        {
            "name": "Carlos Rodríguez",
            "email": "carlos.rodriguez@unxchange.com",
            "password": "carlos123456",
            "role": UserRole.profesional.value
        },
        {
            "name": "María López",
            "email": "maria.lopez@unxchange.com",
            "password": "maria123456",
            "role": UserRole.administrador.value
        },
        {
            "name": "Diego Martínez",
            "email": "diego.martinez@unxchange.com",
            "password": "diego123456",
            "role": UserRole.estudiante.value
        },
        {
            "name": "Sofia Hernández",
            "email": "sofia.hernandez@unxchange.com",
            "password": "sofia123456",
            "role": UserRole.profesional.value
        }
    ]
    
    # Crear sesión de base de datos
    db: Session = SessionLocal()
    
    try:
        created_users = []
        
        for user_data in test_users:
            # Verificar si el usuario ya existe
            existing_user = db.query(User).filter(User.email == user_data["email"]).first()
            
            if existing_user:
                print(f"⚠️  Usuario {user_data['email']} ya existe. Saltando...")
                continue
            
            # Crear nuevo usuario
            hashed_password = get_password_hash(user_data["password"])
            
            new_user = User(
                name=user_data["name"],
                email=user_data["email"],
                hashed_password=hashed_password,
                role=user_data["role"]
            )
            
            db.add(new_user)
            created_users.append(user_data)
        
        # Confirmar los cambios
        db.commit()
        
        # Mostrar resultados
        if created_users:
            print(f"✅ Se crearon {len(created_users)} usuarios exitosamente:")
            for user in created_users:
                print(f"   📧 {user['email']} - {user['name']} ({user['role']})")
        else:
            print("ℹ️  No se crearon usuarios nuevos (todos ya existían)")
            
        print(f"\n📊 Total de usuarios en la base de datos: {db.query(User).count()}")
        
    except IntegrityError as e:
        db.rollback()
        print(f"❌ Error de integridad en la base de datos: {e}")
        
    except Exception as e:
        db.rollback()
        print(f"❌ Error inesperado: {e}")
        
    finally:
        db.close()

def main():
    """Función principal del script."""
    print("🚀 Iniciando inserción de usuarios de prueba...")
    print("=" * 50)
    
    try:
        create_test_users()
        
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        sys.exit(1)
    
    print("=" * 50)
    print("✨ Script completado")

if __name__ == "__main__":
    main()