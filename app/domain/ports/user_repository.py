"""
Puerto para el repositorio de usuarios.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import Usuario


class UsuarioRepository(ABC):
    """Interfaz para el repositorio de usuarios."""

    @abstractmethod
    def save(self, usuario: Usuario) -> Usuario:
        """Guarda un usuario en el repositorio."""
        pass

    @abstractmethod
    def find_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Busca un usuario por su ID."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por su email."""
        pass

    @abstractmethod
    def find_by_cliente_id(self, cliente_id: int) -> List[Usuario]:
        """Busca usuarios por ID de cliente."""
        pass

    @abstractmethod
    def find_all(self) -> List[Usuario]:
        """Retorna todos los usuarios."""
        pass

    @abstractmethod
    def delete(self, usuario_id: int) -> bool:
        """Elimina un usuario del repositorio."""
        pass

    @abstractmethod
    def update(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario en el repositorio."""
        pass