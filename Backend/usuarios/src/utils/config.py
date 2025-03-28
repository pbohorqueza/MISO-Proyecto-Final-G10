from dotenv import load_dotenv
import os

class Config:
    """Configuración base"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    def __init__(self, env_file):
        load_dotenv(env_file)
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_PORT = os.getenv("DB_PORT")
        self.DB_NAME = os.getenv("DB_NAME")
        self.USUARIOS_PATH = os.getenv("USUARIOS_PATH")

class DevelopmentConfig(Config):
    """Configuración para el entorno de desarrollo"""
    def __init__(self):
        super().__init__('.env.development')

class TestingConfig(Config):
    """Configuración para el entorno de pruebas"""
    def __init__(self):
        super().__init__('.env.test')

class ProductionConfig(Config):
    """Configuración para el entorno de producción"""
    def __init__(self):
        super().__init__('.env')


def get_config(env_name):
    """Obtén la configuración según el entorno"""
    if env_name == 'development':
        return DevelopmentConfig()
    elif env_name == 'test':
        return TestingConfig()
    elif env_name == 'production':
        return ProductionConfig()
    else:
        raise ValueError("Invalid environment name")
