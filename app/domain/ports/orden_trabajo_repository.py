"""
Puerto para el repositorio de órdenes de trabajo.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.orden_trabajo import OrdenDeTrabajo


class OrdenTrabajoRepository(ABC):
    """Interfaz para el repositorio de órdenes de trabajo."""

    @abstractmethod
    def save(self, orden: OrdenDeTrabajo) -> OrdenDeTrabajo:
        """Guarda una orden de trabajo en el repositorio."""
        pass

    @abstractmethod
    def find_by_id(self, orden_id: int) -> Optional[OrdenDeTrabajo]:
        """Busca una orden de trabajo por su ID."""
        pass

    @abstractmethod
    def find_by_cliente_id(self, cliente_id: int) -> List[OrdenDeTrabajo]:
        """Busca órdenes de trabajo por ID de cliente."""
        pass

    @abstractmethod
    def find_by_status(self, status: str) -> List[OrdenDeTrabajo]:
        """Busca órdenes de trabajo por su estado."""
        pass

    @abstractmethod
    def find_all(self) -> List[OrdenDeTrabajo]:
        """Retorna todas las órdenes de trabajo."""
        pass

    @abstractmethod
    def delete(self, orden_id: int) -> bool:
        """Elimina una orden de trabajo del repositorio."""
        pass

    @abstractmethod
    def update(self, orden: OrdenDeTrabajo) -> OrdenDeTrabajo:
        """Actualiza una orden de trabajo en el repositorio."""
        pass