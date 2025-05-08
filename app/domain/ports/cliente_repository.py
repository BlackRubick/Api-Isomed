"""
Puerto para el repositorio de clientes.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.cliente import Cliente


class ClienteRepository(ABC):
    """Interfaz para el repositorio de clientes."""

    @abstractmethod
    def save(self, cliente: Cliente) -> Cliente:
        """Guarda un cliente en el repositorio."""
        pass

    @abstractmethod
    def find_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca un cliente por su ID."""
        pass

    @abstractmethod
    def find_by_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por su nombre."""
        pass

    @abstractmethod
    def find_all(self) -> List[Cliente]:
        """Retorna todos los clientes."""
        pass

    @abstractmethod
    def delete(self, cliente_id: int) -> bool:
        """Elimina un cliente del repositorio."""
        pass

    @abstractmethod
    def update(self, cliente: Cliente) -> Cliente:
        """Actualiza un cliente en el repositorio."""
        pass