from flask import request, jsonify, current_app
from functools import wraps
import os
from werkzeug.exceptions import Unauthorized
import requests
from app.config.application import ApplicationConfig


def validate_token(f):
    """
    Decorator to validate token with the usuarios microservice.
    This replaces the JWT authentication in a microservices architecture.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({'message': 'Missing authorization header'}), 401

        # In a real implementation, make a request to the usuarios microservice
        # to validate the token. Here's a placeholder for the actual implementation.
        try:
            # Example of how to call the usuarios microservice
            response = requests.get(
                f"{ApplicationConfig.USERS_SERVICE_URL}/me",
                headers={'Authorization': auth_header}
            )

            if response.status_code != 200:
                return jsonify({'message': 'Invalid or expired token'}), 401

            user_data = response.json()

            # Attach the user_data to the request context
            request.user = user_data

            # Continue to the original function
            return f(*args, **kwargs)
        except requests.exceptions.RequestException as e:
            return jsonify({'message': f'Authentication error: {str(e)}'}), 401

    return decorated_function


def director_required(f):
    """
    Decorator to ensure the user has the ADMINISTRADOR role.
    This should be used after the validate_token decorator.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(request, 'user'):
            return jsonify({'message': 'Authentication required'}), 401

        if request.user.get('rol') != 'ADMINISTRADOR':
            return jsonify({'message': 'Permission denied. Director role required'}), 403

        return f(*args, **kwargs)

    return decorated_function
