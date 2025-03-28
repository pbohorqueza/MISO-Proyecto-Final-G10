from .base_command import BaseCommannd
from src.db.session import SessionLocal
from src.errors.errors import InvalidUsuarioData, UsuarioNotFound
from src.models.usuario import Usuario

class Update(BaseCommannd):
    def __init__(self, uid, data):
        self.uid = uid
        self.data = data
  
    def execute(self):
        # Validar datos
        if not self.is_valid():
            raise InvalidUsuarioData
        # Nueva Session
        db = SessionLocal()
        try:
            # Buscar el usuario por ID
            current_usuario = db.query(Usuario).filter_by(id=self.uid).first()
            if not current_usuario:
                raise UsuarioNotFound
            
            current_usuario.nombre = self.data["nombre"]
            current_usuario.apellido = self.data["apellido"]
            db.commit()
            
            return {
                "msg": "el usuario ha sido actualizado"
            }

        except Exception as e:
            db.rollback()
            raise e
    
    def is_valid(self):
        return all(field in self.data for field in ['nombre', 'apellido'])
    
    