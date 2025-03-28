from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from src.utils.config import get_config
import os

env_name = os.getenv('FLASK_ENV', 'development')
config = get_config(env_name)

# motor de base de datos
print(f"env_name: {env_name}")
if env_name == 'test':
    DATABASE_URL = 'sqlite:///:memory:'  # Usar SQLite en memoria para pruebas
else:
    DATABASE_URL = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"

# DATABASE_URL = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}"
print(f"Connecting to database: {DATABASE_URL}")

# engine = create_engine("postgresql://${sdc}:postgres@localhost:5432/usuarios")
engine = create_engine(DATABASE_URL)
#inspector = inspect(engine)

def get_inspector(engine):
    return inspect(engine)

# clase SessionLocal para manejar las sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
