"""
Configuración y variables de entorno.
"""
import os
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    # Configuración general
    APP_NAME: str = Field("ISOMED API", env="APP_NAME")
    DEBUG: bool = Field(True, env="DEBUG")

    # Configuración de la base de datos
    DATABASE_URL: str = Field(
        os.environ.get("DATABASE_URL", "mysql+pymysql://root:manuel@localhost:3306/isomed")
    )

    # Configuración JWT
    SECRET_KEY: str = Field(
        os.environ.get("SECRET_KEY", "tu_clave_secreta_muy_segura_aqui")
    )
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # CORS
    CORS_ORIGINS: list = ["*"]
    model_config = {"env_file": ".env"}

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        """
        Formatea la URL de la base de datos para ser compatible con SQLAlchemy.
        Maneja específicamente conexiones a Railway.
        """
        url = self.DATABASE_URL
        # Si es una URL de Railway o cualquier proveedor en la nube
        if "localhost" not in url and "127.0.0.1" not in url:
            # Asegurarse de que tiene los parámetros necesarios para MySQL 8
            if "?" not in url:
                url += "?charset=utf8mb4"
            else:
                url += "&charset=utf8mb4"
        return url