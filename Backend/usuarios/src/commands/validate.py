from .base_command import BaseCommannd
from src.db.session import SessionLocal
from datetime import datetime
from src.errors.errors import Forbidden, Unauthorized

from src.models.usuario import Usuario

class Validate(BaseCommannd):
    def __init__(self, token):
        self.token = token
  
    def execute(self):
        # Validar datos
        if not self.token:
            raise Forbidden
        # Crear usuario
        db = SessionLocal()
        try:
            # Obtener el token
            print(f"Token: {self.token}")
            current_token = self.token.split(" ")[1]
            # Buscar el usuario por token
            print(f"Buscar usuario por token: {current_token}")
            current_usuario = db.query(Usuario).filter_by(token=current_token).first()
            
            if not current_usuario:
                raise Unauthorized
            
            if current_usuario.expireAt and current_usuario.expireAt < datetime.now():
                raise Unauthorized
            
            return {
                "id": current_usuario.id,
                "username": current_usuario.username,
                "nombre": current_usuario.nombre,
                "apellido": current_usuario.apellido,
                "rol": current_usuario.rol.value
            }

        except Exception as e:
            db.rollback()
            raise e