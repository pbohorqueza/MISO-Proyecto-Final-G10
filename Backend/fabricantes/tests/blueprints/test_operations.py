import pytest

from src.db.session import SessionLocal
from src.models.fabricante import Fabricante


@pytest.fixture
def valid_fabricante_data():
    return {
        "nombre": "Alpina",
        "numeroTel": "3211466",
        "representante": "Andres Garcia",
    }


# before each
@pytest.fixture
def session():
    yield
    db = SessionLocal()
    db.query(Fabricante).delete()
    db.commit()
    db.close()


def test_check_health(client):
    response = client.get('/fabricantes/ping')
    assert response.status_code == 200
    assert response.data == b"success"


def test_reset_database(client):
    response = client.post('/fabricantes/reset')
    assert response.status_code == 200


def test_create_fabricante_success(client, valid_fabricante_data):
    response = client.post('/fabricantes', json=valid_fabricante_data, headers={'Authorization': 'Bearer 1234'})
    assert response.status_code == 201
    


def test_cannot_create_fabricante_without_token(client, valid_fabricante_data):
    response = client.post('/fabricantes', json=valid_fabricante_data)

    assert response.status_code == 403


def test_cannot_create_fabricante_with_invalid_token(client, valid_fabricante_data):
    response = client.post('/fabricantes', json=valid_fabricante_data, headers={'Authorization ': 'Bearer 1234'})

    assert response.status_code == 403


def test_cannot_create_fabricante_with_missing_fields(client, valid_fabricante_data):
    
    invalid_data = valid_fabricante_data.copy()
    invalid_data.pop("nombre", None)
    
    response = client.post('/fabricantes', json=invalid_data, headers={'Authorization': 'Bearer 1234'})

    json_response = response.get_json()

    assert response.status_code == 400
    assert "nombre" in json_response["msg"]


def test_list_fabricantes(client, valid_fabricante_data):
   
    client.post('/fabricantes', json=valid_fabricante_data, headers={"Authorization": "Bearer 1234"})

    response = client.get('/fabricantes', headers={'Authorization': 'Bearer 1234'})

    assert response.status_code == 200
    assert len(response.get_json()) == 1

# Fabricante filtrado por nombre
def test_list_nombre(client, valid_fabricante_data):
    
    new_fabricante = valid_fabricante_data.copy()
    
    client.post('/fabricantes', json=valid_fabricante_data, headers={'Authorization': 'Bearer 1234'})
    
    #print(new_fabricante["nombre"])
    response = client.get('/fabricantes?flight=' + new_fabricante["nombre"], headers={'Authorization': 'Bearer 1234'})

    assert response.status_code == 200
    assert len(response.get_json()) == 1