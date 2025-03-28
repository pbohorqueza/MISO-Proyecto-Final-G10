from .base_command import BaseCommannd
from src.db.session import SessionLocal
from datetime import datetime
from src.errors.errors import InvalidUsuarioData, UsuarioAlreadyExists
from src.models.usuario import Usuario
import re
import bcrypt

class Create(BaseCommannd):
    def __init__(self, data):
        self.data = data

    def execute(self):
        # Validar datos
        if not self.is_valid():
            raise InvalidUsuarioData
        # Crear usuario
        db = SessionLocal()
        try:
            usuario_exists = db.query(Usuario).filter(Usuario.username == self.data['username']).first()
            if usuario_exists:
                raise UsuarioAlreadyExists
            
            
            if not self.username_is_valid(self.data['username']):
                raise InvalidUsuarioData
            
            if not self.password_is_valid(self.data['password']):
                raise InvalidUsuarioData
            
            
            hash_pawd, salt = self.hash_password(self.data['password'])

            new_usuario = Usuario(
                username=self.data['username'],
                password=hash_pawd,
                nombre=self.data.get('nombre'),
                apellido=self.data.get('apellido'),
                rol=self.data.get('rol'),
                salt=salt,
                token="",
                expireAt=datetime.now()
            )
            db.add(new_usuario)
            db.commit()
            
            return {
                "id": new_usuario.id,
                "createdAt": new_usuario.createdAt.isoformat(),
            }

        except Exception as e:
            db.rollback()
            raise e
    
    def is_valid(self):
        return all(field in self.data for field in ['username', 'password', 'nombre', 'apellido', 'rol'])
    
    def username_is_valid(self, username):
        pattern = r'^[a-zA-Z0-9]+$'
        return re.match(pattern, username) and len(username) > 0
    
    def password_is_valid(self, password):
        return len(password) > 0
    
    def hash_password(self, password):
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8'), salt