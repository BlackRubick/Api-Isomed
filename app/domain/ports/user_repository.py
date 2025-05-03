"""
Puerto para el repositorio de usuarios.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.user import User


class UserRepository(ABC):
    """Interfaz para el repositorio de usuarios."""

    @abstractmethod
    def save(self, user: User) -> User:
        """Guarda un usuario en el repositorio."""
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID."""
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su email."""
        pass

    @abstractmethod
    def find_all(self) -> List[User]:
        """Retorna todos los usuarios."""
        pass

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Elimina un usuario del repositorio."""
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """Actualiza un usuario en el repositorio."""
        pass