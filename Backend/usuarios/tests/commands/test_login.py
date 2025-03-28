import pytest
from unittest.mock import patch, MagicMock
from src.commands.login import Login
from src.errors.errors import InvalidUsuarioData, UsuarioNotFound
import bcrypt

@pytest.fixture
def mock_session():
    with patch('src.commands.login.SessionLocal') as MockSessionLocal:
        mock_session = MagicMock()
        MockSessionLocal.return_value = mock_session
        yield mock_session

def test_login_success(mock_session):
    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    
    # Configurar el mock para simular un usuario existente
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    mock_usuario = MagicMock()
    mock_usuario.password = hashed_password
    mock_session.query().filter_by().first.return_value = mock_usuario
    mock_session.commit = MagicMock()
    
    login_command = Login(data)
    result = login_command.execute()
    
    assert 'token' in result
    assert 'expireAt' in result
    assert mock_usuario.token == result['token']
    assert mock_usuario.expireAt == result['expireAt']
    mock_session.commit.assert_called_once()

def test_login_usuario_not_found(mock_session):
    data = {
        'username': 'nonexistentuser',
        'password': 'testpassword'
    }
    
    # Configurar el mock para simular que no se encuentra el usuario
    mock_session.query().filter_by().first.return_value = None
    
    login_command = Login(data)
    
    with pytest.raises(UsuarioNotFound):
        login_command.execute()

def test_login_invalid_password(mock_session):
    data = {
        'username': 'testuser',
        'password': 'wrongpassword'
    }
    
    # Configurar el mock para simular un usuario existente con una contraseña diferente
    correct_password = 'correctpassword'
    hashed_password = bcrypt.hashpw(correct_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    mock_usuario = MagicMock()
    mock_usuario.password = hashed_password
    mock_session.query().filter_by().first.return_value = mock_usuario
    
    login_command = Login(data)
    
    with pytest.raises(UsuarioNotFound):
        login_command.execute()

def test_login_invalid_data(mock_session):
    data = {
        'username': 'testuser'
        # Falta el campo 'password'
    }
    
    login_command = Login(data)
    
    with pytest.raises(InvalidUsuarioData):
        login_command.execute()

def test_login_exception(mock_session):
    data = {
        'username': 'testuser',
        'password': 'testpassword'
    }
    
    # Configurar el mock para levantar una excepción
    mock_session.query().filter_by().first.side_effect = Exception("Database error")
    
    login_command = Login(data)
    
    with pytest.raises(Exception) as excinfo:
        login_command.execute()
    
    assert str(excinfo.value) == "Database error"
    mock_session.rollback.assert_called_once()
