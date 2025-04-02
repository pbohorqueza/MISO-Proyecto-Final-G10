from sqlalchemy import Column, String, Boolean, DateTime, Float
from src.db.base import Base
from .model import Model

class Categoria(enum.Enum):
    ALIMENTOS_BEBIDAS = "ALIMENTOS Y BEBIDAS"
    CUIDADO_PERSONAL = "CUIDADO PERSONAL"
    LIMPIEZA_HOGAR = "LIMPIEZA Y HOGAR"
    BEBES = "BEBÉS"
    MASCOTAS = "MASCOTAS"

class Producto(Base, Model):
    __tablename__ = 'Producto'
    sku = Column(String, primary_key=True, nullable=False)  #SKU calculado como id fabricante+id producto
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    perecedero = Column(Boolean, nullable=False)
    fechaVencimiento = Column(DateTime, nullable=False)
    valorUnidad = Column(Float, nullable=False)
    tiempoEntrega = Column(DateTime, nullable=False)
    condicionAlmacenamiento = Column(String, nullable=False)
    reglasLegales = Column(String, nullable=False)
    reglasComerciales = Column(String, nullable=False)
    reglasTributarias = Column(String, nullable=False)
    categoria = Column(db.Enum(Categoria), nullable=False)
    fabricante_id = Column(String, nullable=False) #Almacena el id del Fabricante asociado

    