from flask import jsonify
from marshmallow import ValidationError, Schema, fields

from src.db.session import SessionLocal
from src.errors.errors import InvalidFabricanteData
from src.models.fabricante import Fabricante
from .base_command import BaseCommand


class CreateFabricanteSchema(Schema):
    nombre = fields.Str(required=True)
    numeroTel = fields.Str(required=True)
    representante = fields.Str(required=True)

class Create(BaseCommand):
    def __init__(self, usuario, data):
        self.usuario = usuario
        self.data = data

    def execute(self):
        schema = self.safe_payload()
        db = SessionLocal()

        try:
            existing_fabricante = db.query(Fabricante).filter_by(nombre=schema['nombre']).first()
            if existing_fabricante:
                raise InvalidFabricanteData('El fabricante ya existe')
            
            new_fabricante = Fabricante(
                nombre=schema['nombre'],
                numeroTel=schema['numeroTel'],
                representante=schema['representante']
            )

            db.add(new_fabricante)
            db.commit()

            return {
                "id": new_fabricante.id,
                "createdAt": new_fabricante.createdAt.isoformat()
            }

        except Exception as e:
            db.rollback()
            raise e

    def safe_payload(self):
        try:
            schema = CreateFabricanteSchema().load(self.data)
        except ValidationError as e:
            raise InvalidFabricanteData(e.messages)
        

        # add more data validations here or data formatting before CRUD manipulation
        
        return schema