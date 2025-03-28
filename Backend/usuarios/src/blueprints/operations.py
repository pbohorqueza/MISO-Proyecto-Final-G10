from flask import Flask, jsonify, request, Blueprint
from ..commands.create import Create
from ..commands.update import Update
from ..commands.login import Login
from ..commands.clean import Clean
from ..commands.validate import Validate
import os

operations_blueprint = Blueprint('usuarios', __name__)

@operations_blueprint.route('', methods = ['POST'])
def create_usuario():
    json = request.get_json()
    result = Create(json).execute()
    return jsonify(result), 201


@operations_blueprint.route('/<uuid:id>', methods = ['PATCH'])
def update_usuario(id):
    json = request.get_json()
    result = Update(id, json).execute()
    return jsonify(result), 200

@operations_blueprint.route('/auth', methods = ['POST'])
def login_usuario():
    json = request.get_json()
    result = Login(json).execute()
    return jsonify(result), 200


@operations_blueprint.route('/me', methods = ['GET'])
def validate_usuario():
    #Obtener el token de la cabecera
    auth_header = request.headers.get('Authorization')
    result = Validate(auth_header).execute()
    return jsonify(result), 200

# Consulta de salud del servicio
@operations_blueprint.route("/ping", methods = ['GET'])
def health_check():
    return "success", 200

# Restablecer base de datos
@operations_blueprint.route("/reset", methods = ['POST'])
def reset_usuario_database():
    result = Clean().execute()
    return jsonify(result), 200