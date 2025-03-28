from flask import Flask, jsonify, request, Blueprint, g
from ..commands.create import Create
from ..commands.clean import Clean
from src.utils.validate_token import token_required
import os

from ..commands.delete import Delete
from ..commands.list import List
from ..commands.show import Show

operations_blueprint = Blueprint('fabricantes', __name__)

@operations_blueprint.route('', methods=['POST'])
@token_required
def create_fabricante():
    json = request.get_json()
    current_usuario = g.current_usuario

    result = Create(current_usuario, json).execute()

    return jsonify(result), 201


@operations_blueprint.route('', methods=['GET'])
@token_required
def list_fabricantes():
    current_usuario = g.current_usuario

    service = List(
        usuario=current_usuario,
        data=request.args.to_dict()
    )

    fabricantes = service.execute()

    return jsonify(fabricantes), 200


@operations_blueprint.route('/<string:id>', methods=['GET'])
@token_required
def get_fabricante(id):
    result = Show(id).execute()

    return jsonify(result), 200


@operations_blueprint.route('/<string:id>', methods=['DELETE'])
@token_required
def delete_fabricante(id):
    Delete(id).execute()

    return jsonify({
        "msg": "el fabricante fue eliminado"
    }), 200

# Consulta de salud del servicio
@operations_blueprint.route("/ping", methods=['GET'])
def health_check():
    return "success", 200


# Restablecer base de datos
@operations_blueprint.route("/reset", methods=['POST'])
def reset_fabricante_database():
    result = Clean().execute()

    return jsonify(result), 200
