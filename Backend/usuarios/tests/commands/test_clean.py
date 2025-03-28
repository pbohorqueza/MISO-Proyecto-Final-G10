import pytest
from unittest.mock import patch, MagicMock
from src.commands.clean import Clean
from src.models.usuario import Usuario

@pytest.fixture
def mock_session():
    with patch('src.commands.clean.SessionLocal') as MockSessionLocal:
        # Crear un mock para la sesión
        mock_session = MagicMock()
        # Configurar el mock para que devuelva un mock de consulta
        mock_query = MagicMock()
        mock_query.count.return_value = 5  # Simular que hay 5 usuarios en la base de datos
        mock_query.delete.return_value = 5  # Simular que se eliminaron 5 usuarios
        mock_session.query.return_value = mock_query

        MockSessionLocal.return_value = mock_session
        yield mock_session

def test_clean_execute(mock_session):
    clean_command = Clean()

    # Ejecutar el comando
    result = clean_command.execute()

    # Verificar los resultados
    assert result == {"msg": "Todos los datos fueron eliminados"}
    mock_session.query().delete.assert_called_once()
    mock_session.commit.assert_called_once()

def test_clean_no_usuarios(mock_session):
    mock_query = MagicMock()
    mock_query.count.return_value = 0
    mock_query.delete.return_value = 0
    mock_session.query.return_value = mock_query

    # Crear instancia del comando Clean
    clean_command = Clean()

    # Ejecutar el comando
    result = clean_command.execute()

    # Verificar los resultados
    assert result is None
    mock_session.query().delete.assert_not_called()
    mock_session.commit.assert_not_called()

def test_clean_exception():
    with patch('src.commands.clean.SessionLocal') as MockSessionLocal:
        # Crear un mock para la sesión
        mock_session = MagicMock()
        # Configurar el mock para lanzar una excepción cuando se intenta consultar
        mock_session.query.side_effect = Exception("Database error")
        MockSessionLocal.return_value = mock_session

        # Crear instancia del comando Clean
        clean_command = Clean()

        # Ejecutar el comando
        result = clean_command.execute()

        # Verificar los resultados
        
        assert 'error' in result