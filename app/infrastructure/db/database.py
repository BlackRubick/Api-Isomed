"""
Configuración de la base de datos MySQL con SQLAlchemy.
"""
import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.infrastructure.config.settings import Settings

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

settings = Settings()

# Usar la propiedad SQLALCHEMY_DATABASE_URL para obtener la URL formateada
SQLALCHEMY_DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

# Log para debug
logger.info(f"Intentando conectar a la base de datos con URL: {SQLALCHEMY_DATABASE_URL}")

# Crear el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=settings.DEBUG
)

# Crear el fabricante de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear la base para los modelos declarativos
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()