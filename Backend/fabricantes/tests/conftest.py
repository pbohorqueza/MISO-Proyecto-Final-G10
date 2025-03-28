import pytest
import requests

from src.main import create_app
from unittest.mock import patch, MagicMock
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


@pytest.fixture(scope='module')
def session():
    with patch('sqlalchemy.create_engine') as mock_engine, patch('sqlalchemy.inspect') as mock_inspect:
        # Mockeamos el motor de SQLAlchemy
        mock_engine.return_value = MagicMock()

        # Crear un engine falso para las pruebas
        fake_engine = create_engine('sqlite:///:memory:')  # Usar SQLite en memoria para pruebas

        # Mockear el inspector
        mock_inspect.return_value.get_table_names.return_value = []

        # Creamos un sessionmaker usando el motor mockeado
        Session = sessionmaker(bind=fake_engine)
        session = Session()

        yield session

        session.close()


@pytest.fixture(scope='module')
def client():
    app = create_app('test')
    app.config.update({
        "TESTING": True,
    })

    with app.test_client() as client, patch('sqlalchemy.create_engine') as mock_engine, patch(
            'sqlalchemy.inspect') as mock_inspect:
        # Mockeamos el motor de SQLAlchemy
        mock_engine.return_value.connect.return_value = None

        # Mockear el inspector
        mock_inspect.return_value.get_table_names.return_value = []

        yield client


@pytest.fixture
def mock_auth_response(monkeypatch):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    def mock_get(*args, **kwargs):
        return MockResponse({"id": "test_usuario_id"}, 200)

    monkeypatch.setattr(requests, "get", mock_get)
