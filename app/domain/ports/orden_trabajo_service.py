"""
Puerto para el servicio de órdenes de trabajo.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from app.domain.entities.orden_trabajo import OrdenDeTrabajo


class OrdenTrabajoService(ABC):
    """Interfaz para el servicio de órdenes de trabajo."""

    @abstractmethod
    def create_orden(self, orden_data: Dict[str, Any]) -> OrdenDeTrabajo:
        """Crea una nueva orden de trabajo."""
        pass

    @abstractmethod
    def get_orden(self, orden_id: int) -> Optional[OrdenDeTrabajo]:
        """Obtiene una orden de trabajo por su ID."""
        pass

    @abstractmethod
    def get_ordenes_by_cliente(self, cliente_id: int) -> List[OrdenDeTrabajo]:
        """Obtiene todas las órdenes de trabajo de un cliente."""
        pass

    @abstractmethod
    def get_all_ordenes(self) -> List[OrdenDeTrabajo]:
        """Obtiene todas las órdenes de trabajo."""
        pass

    @abstractmethod
    def update_orden(self, orden_id: int, orden_data: Dict[str, Any]) -> OrdenDeTrabajo:
        """Actualiza una orden de trabajo."""
        pass

    @abstractmethod
    def delete_orden(self, orden_id: int) -> bool:
        """Elimina una orden de trabajo."""
        pass