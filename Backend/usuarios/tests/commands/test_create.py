import pytest
from unittest.mock import patch, MagicMock
from src.commands.create import Create
from src.models.usuario import UsuarioRol
from src.errors.errors import InvalidUsuarioData, UsuarioAlreadyExists
from datetime import datetime

@pytest.fixture
def mock_session():
    with patch('src.commands.create.SessionLocal') as MockSessionLocal:
        mock_session = MagicMock()
        MockSessionLocal.return_value = mock_session
        yield mock_session

def test_create_usuario_success(mock_session):
    data = {
        'username': 'testuser',
        'password': 'password123',
        'nombre': 'Test',
        'apellido': 'User',
        'rol': UsuarioRol.ADMINISTRADOR
    }
    
    # Configurar el mock para simular que no hay usuario existente
    mock_session.query().filter().first.return_value = None

    # Configurar el mock para simular la creación del usuario
    mock_usuario = MagicMock()
    mock_usuario.id = 1
    mock_usuario.createdAt = datetime.now()
    mock_session.add = MagicMock()
    mock_session.commit = MagicMock()
    
    # Simular que el nuevo usuario se crea correctamente
    with patch('src.commands.create.Usuario', return_value=mock_usuario):
        create_command = Create(data)
        result = create_command.execute()
        
        assert result == {
            "id": 1,
            "createdAt": mock_usuario.createdAt.isoformat(),
        }
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

def test_create_usuario_invalid_data(mock_session):
    data = {
        'username': 'testuser',
        'nombre': 'testuser'
    }
    
    create_command = Create(data)
    
    with pytest.raises(InvalidUsuarioData):
        create_command.execute()
        

def test_create_usuario_already_exists(mock_session):
    data = {
        'username': 'testuser',
        'password': 'password123'
    }
    
    # Configurar el mock para simular que el usuario ya existe
    mock_session.query().filter().first.return_value = MagicMock()
    
    create_command = Create(data)
    
    with pytest.raises(UsuarioAlreadyExists):
        create_command.execute()
        
def test_create_usuario_invalid_username(mock_session):
    data = {
        'username': 'Juan de la pena!',
        'password': 'password123',
        'nombre': 'Test 2',
        'apellido': 'User 2'
    }
    
    # Configurar el mock para simular que no hay usuario existente
    mock_session.query().filter().first.return_value = None
    
    create_command = Create(data)
    
    with pytest.raises(InvalidUsuarioData):
        create_command.execute()
        
def test_create_usuario_invalid_password(mock_session):
    data = {
        'username': 'Juan',
        'password': '',
        'nombre': 'Test 2',
        'apellido': 'User 2'
    }
    
    # Configurar el mock para simular que no hay usuario existente
    mock_session.query().filter().first.return_value = None
    
    create_command = Create(data)
    
    with pytest.raises(InvalidUsuarioData):
        create_command.execute()

def test_create_usuario_exception(mock_session):
    data = {
        'username': 'testuser',
        'password': 'password123'
    }
    
    # Configurar el mock para levantar una excepción
    mock_session.query().filter().first.side_effect = Exception("Database error")
    
    create_command = Create(data)
    
    with pytest.raises(Exception) as excinfo:
        create_command.execute()
    
    assert str(excinfo.value) == "Database error"
    mock_session.rollback.assert_called_once()
