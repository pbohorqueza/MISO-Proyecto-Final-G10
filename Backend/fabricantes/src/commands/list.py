from marshmallow import ValidationError, Schema, fields

from .base_command import BaseCommand
from ..db.session import SessionLocal
from ..errors.errors import InvalidFabricanteData
from ..models.fabricante import Fabricante
from ..utils.helpers import serialize_sqlalchemy


class ListFabricanteSchema(Schema):
    #Esta linea permite filtrar por nombre del Fabricante
    nombre = fields.Str(required=False)

class List(BaseCommand):
    def __init__(self, usuario, data):
        self.usuario = usuario
        self.data = data

    def execute(self):
        db = SessionLocal()
        payload = self.safe_payload()
        conditions = []
        query = db.query(Fabricante)
        print(payload.get('nombre'))
        
        if payload.get('nombre'):
            conditions.append(Fabricante.nombre == payload['nombre'])

        if conditions:
            query = query.filter(*conditions)

        return serialize_sqlalchemy(query.all())

    def safe_payload(self):
        try:
            schema = ListFabricanteSchema().load(self.data)
        except ValidationError as e:
            raise InvalidFabricanteData(e.messages)

        return schema
