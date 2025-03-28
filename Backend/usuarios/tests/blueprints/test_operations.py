import json
import pytest
from src.commands.create import Create
from src.commands.update import Update
from src.commands.login import Login
from src.commands.validate import Validate
from src.commands.clean import Clean


def test_create_usuario(client):
    # Mock the Create command
    def mock_create(json):
        return {
            "id": "1234",
            "createdAt": "2021-09-01T00:00:00Z",
        }
    
    # Replace Create.execute with the mock
    original_create = Create.execute
    Create.execute = mock_create
    
    usuario_json = {
        "username": "enola",
        "password": "gd5kv2d8gapjnrz",
        "nombre": "Bradley",
        "apellido": "Veum"
    }

    response = client.post('/usuarios', json=usuario_json)
    response_json = json.loads(response.data)

    assert response.status_code == 201
    assert 'id' in response_json

    # Restore the original method
    Create.execute = original_create



def test_update_usuario(client):
    # Mock the Update command
    def mock_update(json):
        return {
            "msg": "el usuario ha sido actualizado"
        }
    
    # Replace Update.execute with the mock
    original_update = Update.execute
    Update.execute = mock_update
    
    usuario_json = {
        "nombre": "Eileen",
        "apellido": "Abernathy"
    }

    response = client.patch('/usuarios/7f201377-fa82-43e5-8f2e-1cbb3874f56f', json=usuario_json)
    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert 'msg' in response_json

    # Restore the original method
    Update.execute = original_update

def test_login_usuario(client):
    # Mock the Login command
    def mock_login(json):
        return {"token": "abc123"}

    # Replace Login.execute with the mock
    original_login = Login.execute
    Login.execute = mock_login

    response = client.post('/usuarios/auth', json={'username': 'test', 'password': 'pass'})
    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert 'token' in response_json
    assert response_json['token'] == 'abc123'

    # Restore the original method
    Login.execute = original_login
    

def test_validate_usuario(client):
    # Mock the Validate command
    def mock_validate(auth_header):
        return {
            "nombre": "Jodi",
            "apellido": "Steuber",
            "id": "ad60d00e-c30e-4e22-9b51-4447057131a4",
            "rol": "ADMINISTRADOR",
            "username": "jodi steuber"
        }

    # Replace Validate.execute with the mock
    original_validate = Validate.execute
    Validate.execute = mock_validate

    response = client.get('/usuarios/me', headers={'Authorization': 'Bearer token'})
    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert 'nombre' in response_json
    assert 'apellido' in response_json
    assert 'id' in response_json
    assert 'rol' in response_json
    assert 'username' in response_json
    assert response_json['username'] == "jodi steuber"

    # Restore the original method
    Validate.execute = original_validate

def test_health_check(client):
    response = client.get('/usuarios/ping')
    assert response.status_code == 200
    assert response.data == b"success"

def test_reset_usuario_database(client):
    # Mock the Clean command
    def mock_clean(json):
        return {"msg": "Todos los datos fueron eliminados"}

    # Replace Clean.execute with the mock
    original_clean = Clean.execute
    Clean.execute = mock_clean

    response = client.post('/usuarios/reset')
    response_json = json.loads(response.data)

    assert response.status_code == 200
    assert 'msg' in response_json
    assert response_json['msg'] == "Todos los datos fueron eliminados"

    # Restore the original method
    Clean.execute = original_clean
