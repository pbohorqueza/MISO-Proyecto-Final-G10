from sqlalchemy import Column, String, DateTime, Enum
from src.db.base import Base
from .model import Model
import enum

class UsuarioRol(enum.Enum):
    ADMINISTRADOR = "ADMINISTRADOR"
    TENDERO = "TENDERO"
    VENDEDOR = "VENDEDOR"
    LOGISTICA = "LOGISTICA"

class Usuario(Base, Model):
    __tablename__ = 'Usuario'
    
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nombre = Column(String)
    apellido = Column(String)
    rol = Column(Enum(UsuarioRol), nullable=False)
    
    salt = Column(String, nullable=False)
    token = Column(String)
    expireAt = Column(DateTime)