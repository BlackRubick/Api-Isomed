"""
Configuración y variables de entorno.
"""
from pydantic import Field
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

# Cargar variables de entorno desde archivo .env si existe
load_dotenv()


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    # Configuración general
    APP_NAME: str = Field("ISOMED API", env="APP_NAME")
    DEBUG: bool = Field(True, env="DEBUG")

    # Configuración de la base de datos
    DATABASE_URL: str = Field("mysql+pymysql://root:manuel@localhost:3306/isomed", env="DATABASE_URL")

    # Configuración JWT
    SECRET_KEY: str = Field("tu_clave_secreta_muy_segura_aqui", env="SECRET_KEY")
    JWT_ALGORITHM: str = Field("HS256", env="JWT_ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    # CORS
    CORS_ORIGINS: list = ["*"]
    model_config = {"env_file": ".env"}