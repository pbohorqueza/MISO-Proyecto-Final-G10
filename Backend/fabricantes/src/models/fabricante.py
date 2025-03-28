from sqlalchemy import Column, String
from src.db.base import Base
from .model import Model

class Fabricante(Base, Model):
    __tablename__ = 'Fabricante'
    
    nombre = Column(String, nullable=False)
    numeroTel = Column(String, nullable=False)
    representante = Column(String, nullable=False)
    