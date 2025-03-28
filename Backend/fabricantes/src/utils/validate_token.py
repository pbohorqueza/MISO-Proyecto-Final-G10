from flask import request, jsonify, g
from functools import wraps
import requests
from .config import get_config
import os

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]  # Obtener el token
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        
        try:
            env_name = os.getenv('FLASK_ENV', 'development')
            envData = get_config(env_name)
            usuarios_path = envData.USUARIOS_PATH + '/usuarios/me'
            print(f"Validating token in {usuarios_path} - current token: {token}")
            response = requests.get(usuarios_path, headers={"Authorization": f"Bearer {token}"})
            if response.status_code != 200:
                return jsonify({'message': 'Token is invalid or expired!'}), 401
            g.current_usuario = response.json()
        except Exception as e:
            print(f"Error while validating token: {e}")
            return jsonify({'message': 'Token is invalid or expired!'}), 401
        
        return f(*args, **kwargs)

    return decorated