from .base_command import BaseCommannd
from src.db.session import SessionLocal
from datetime import datetime, timedelta
import bcrypt
import uuid
from src.errors.errors import InvalidUsuarioData, UsuarioNotFound
from src.models.usuario import Usuario

class Login(BaseCommannd):
    def __init__(self, data):
        self.data = data
  
    def execute(self):
        # Validar datos
        if not self.is_valid():
            raise InvalidUsuarioData
        # Crear usuario
        db = SessionLocal()
        try:
            # Buscar el usuario por username
            current_usuario = db.query(Usuario).filter_by(username=self.data["username"]).first()
            if not current_usuario:
                raise UsuarioNotFound
            
            if not self.check_password(self.data['password'], current_usuario.password):
                raise UsuarioNotFound
            
            # Generar un nuevo token
            token = str(uuid.uuid4())
            # Establecer la expiración del token
            token_expiration = datetime.now() + timedelta(days=90)  # expiración: 3 meses (99 dias)
            expire_at = token_expiration.isoformat()
            
            current_usuario.token = token
            current_usuario.expireAt = expire_at
            db.commit()
            
            return {
                "id": current_usuario.id,
                "token": token,
                "expireAt": expire_at
            }

        except Exception as e:
            db.rollback()
            raise e
    
    def is_valid(self):
        return all(field in self.data for field in ['username', 'password'])
    
    
    def check_password(self, current_password, password):
        """
        Verifica si la contraseña proporcionada coincide con la contraseña almacenada
        """
        return bcrypt.checkpw(current_password.encode('utf-8'), password.encode('utf-8'))
    
