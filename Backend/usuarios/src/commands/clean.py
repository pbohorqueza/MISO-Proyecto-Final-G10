from .base_command import BaseCommannd
from src.db.session import engine, SessionLocal
from src.models.usuario import Usuario

class Clean(BaseCommannd):
  def __init__(self):
      pass
  
  def execute(self):
    try:
        session = SessionLocal()
        # Crear una conexión al motor
        with engine.connect() as connection:
            # Obtener cantidad de registros
            usuarioLen = session.query(Usuario).count()
            if usuarioLen == 0:
                return

            # Eliminar todos los registros
            session.query(Usuario).delete()
            session.commit()
            print(f"Se eliminaron {usuarioLen} registros")
        return {"msg": "Todos los datos fueron eliminados"}
    except Exception as e:
        print(f"Error al eliminar datos: {str(e)}")
        return {"error": str(e)}

    