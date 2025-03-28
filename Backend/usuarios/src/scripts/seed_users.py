#!/usr/bin/env python
"""
Script to create test users for each role in the application.
Run this script to populate your database with test users.
"""
from src.db.session import SessionLocal
from src.models.usuario import Usuario, UsuarioRol
import bcrypt
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to sys.path to ensure imports work correctly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


def create_test_user(username, password, nombre, apellido, rol):
    """Create a test user with the specified attributes"""
    db = SessionLocal()
    try:
        # Check if user already exists
        user_exists = db.query(Usuario).filter(Usuario.username == username).first()
        if user_exists:
            print(f'Usuario {username} ya existe.')
            return
            
        # Generate password hash
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Set expiration date to 3 months from now
        expiration_date = datetime.now() + timedelta(days=90)  # expiración: 3 meses (90 dias)
        
        # Create new user
        new_user = Usuario(
            username=username,
            password=hashed_password.decode('utf-8'),
            nombre=nombre,
            apellido=apellido,
            rol=rol,
            salt=salt,
            token="",
            expireAt=expiration_date
        )
        db.add(new_user)
        db.commit()
        print(f'Usuario {username} ({rol.value}) creado con éxito.')
        return new_user.id
    except Exception as e:
        db.rollback()
        print(f'Error al crear usuario {username}: {str(e)}')
    finally:
        db.close()


def seed_all_users():
    """Create test users for all roles"""
    print("Creando usuarios de prueba...")
    
    # Create admin user
    admin_id = create_test_user(
        "admin", 
        "admin123", 
        "Administrador", 
        "Sistema", 
        UsuarioRol.ADMINISTRADOR
    )
    
    # Create tendero user
    tendero_id = create_test_user(
        "tendero", 
        "tendero123", 
        "Tendero", 
        "Prueba", 
        UsuarioRol.TENDERO
    )
    
    # Create vendedor user
    vendedor_id = create_test_user(
        "vendedor", 
        "vendedor123", 
        "Vendedor", 
        "Prueba", 
        UsuarioRol.VENDEDOR
    )
    
    # Create logistica user
    logistica_id = create_test_user(
        "logistica", 
        "logistica123", 
        "Logistica", 
        "Prueba", 
        UsuarioRol.LOGISTICA
    )
    
    print("Proceso de creación de usuarios de prueba completado.")


if __name__ == "__main__":
    seed_all_users()
