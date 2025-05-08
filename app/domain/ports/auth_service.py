"""
Puerto para el servicio de autenticación.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.domain.entities.user import Usuario


class AuthService(ABC):
    """Interfaz para el servicio de autenticación."""

    @abstractmethod
    def register(self, user_data: Dict[str, Any]) -> Usuario:
        """Registra un nuevo usuario."""
        pass

    @abstractmethod
    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica a un usuario y devuelve el token si es exitoso."""
        pass

    @abstractmethod
    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Valida un token y devuelve la información del usuario."""
        pass