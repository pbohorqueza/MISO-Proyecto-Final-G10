import pytest
from unittest.mock import patch, MagicMock
from src.commands.update import Update
from src.errors.errors import InvalidUsuarioData, UsuarioNotFound
from src.models.usuario import UsuarioRol

@pytest.fixture
def mock_session():
    with patch('src.commands.update.SessionLocal') as MockSessionLocal:
        mock_session = MagicMock()
        MockSessionLocal.return_value = mock_session
        yield mock_session

def test_update_usuario_success(mock_session):
    uid = 1
    data = {
        'rol': UsuarioRol.ADMINISTRADOR,
        'nombre': 'Test',
        'apellido': 'User'
    }
    
    # Configurar el mock para simular que se encuentra el usuario
    mock_usuario = MagicMock()
    mock_session.query().filter_by().first.return_value = mock_usuario
    mock_session.commit = MagicMock()
    
    update_command = Update(uid, data)
    result = update_command.execute()
    
    assert result == {"msg": "el usuario ha sido actualizado"}
    assert mock_usuario.rol == UsuarioRol.ADMINISTRADOR
    assert mock_usuario.nombre == 'Test'
    assert mock_usuario.apellido == 'User'
    mock_session.commit.assert_called_once()

def test_update_usuario_not_found(mock_session):
    uid = 1
    data = {
        'rol': UsuarioRol.ADMINISTRADOR,
        'nombre': 'Test',
        'apellido': 'User'
    }
    
    # Configurar el mock para simular que no se encuentra el usuario
    mock_session.query().filter_by().first.return_value = None
    
    update_command = Update(uid, data)
    
    with pytest.raises(UsuarioNotFound):
        update_command.execute()

def test_update_usuario_invalid_data(mock_session):
    uid = 1
    data = {
        'nombre': 'Test',
        'apellido': 'User'
        #falta el campo rol
    }
    
    update_command = Update(uid, data)
    
    with pytest.raises(InvalidUsuarioData):
        update_command.execute()

def test_update_usuario_exception(mock_session):
    uid = 1
    data = {
        'rol': UsuarioRol.ADMINISTRADOR,
        'nombre': 'Test',
        'apellido': 'User'
    }
    
    # Configurar el mock para levantar una excepción
    mock_session.query().filter_by().first.side_effect = Exception("Database error")
    
    update_command = Update(uid, data)
    
    with pytest.raises(Exception) as excinfo:
        update_command.execute()
    
    assert str(excinfo.value) == "Database error"
    mock_session.rollback.assert_called_once()
