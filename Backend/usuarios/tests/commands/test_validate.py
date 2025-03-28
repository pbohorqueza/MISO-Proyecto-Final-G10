import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from src.commands.validate import Validate
from src.errors.errors import Forbidden, Unauthorized

@pytest.fixture
def mock_session():
    with patch('src.commands.validate.SessionLocal') as MockSessionLocal:
        mock_session = MagicMock()
        MockSessionLocal.return_value = mock_session
        yield mock_session

def test_validate_success(mock_session):
    token = "Bearer valid_token"
    
    # Configurar el mock para simular un usuario existente con un token válido y no expirado
    mock_usuario = MagicMock()
    mock_usuario.token = "valid_token"
    mock_usuario.expireAt = datetime.now() + timedelta(hours=1)
    mock_session.query().filter_by().first.return_value = mock_usuario
    
    validate_command = Validate(token)
    result = validate_command.execute()
    
    assert result['id'] == mock_usuario.id
    assert result['username'] == mock_usuario.username
    assert result['nombre'] == mock_usuario.nombre
    assert result['apellido'] == mock_usuario.apellido
    assert result['rol'] == mock_usuario.rol.value

def test_validate_no_token():
    token = ""
    
    validate_command = Validate(token)
    
    with pytest.raises(Forbidden):
        validate_command.execute()

def test_validate_usuario_not_found(mock_session):
    token = "Bearer invalid_token"
    
    # Configurar el mock para simular que no se encuentra un usuario con el token dado
    mock_session.query().filter_by().first.return_value = None
    
    validate_command = Validate(token)
    
    with pytest.raises(Unauthorized):
        validate_command.execute()

def test_validate_token_expired(mock_session):
    token = "Bearer expired_token"
    
    # Configurar el mock para simular un usuario existente pero con el token expirado
    mock_usuario = MagicMock()
    mock_usuario.token = "expired_token"
    mock_usuario.expireAt = datetime.now() - timedelta(hours=1)
    mock_session.query().filter_by().first.return_value = mock_usuario
    
    validate_command = Validate(token)
    
    with pytest.raises(Unauthorized):
        validate_command.execute()

def test_validate_exception(mock_session):
    token = "Bearer valid_token"
    
    # Configurar el mock para levantar una excepción
    mock_session.query().filter_by().first.side_effect = Exception("Database error")
    
    validate_command = Validate(token)
    
    with pytest.raises(Exception) as excinfo:
        validate_command.execute()
    
    assert str(excinfo.value) == "Database error"
    mock_session.rollback.assert_called_once()
