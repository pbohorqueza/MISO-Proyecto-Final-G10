from .base_command import BaseCommand
from src.db.session import engine, SessionLocal
from src.models.fabricante import Fabricante

class Clean(BaseCommand):
  def __init__(self):
      pass
  
  def execute(self):
    try:
        session = SessionLocal()
        with engine.connect() as connection:
            fabricanteLen = session.query(Fabricante).count()
            if fabricanteLen == 0:
                return

            fabricantes = session.query(Fabricante).delete()
            session.commit()
            print(f"Se eliminaron {fabricantes} registros")
        return {"msg": "Todos los datos fueron eliminados"}
    except Exception as e:
        print(f"Error al eliminar datos: {str(e)}")
        return {"error": str(e)}

    