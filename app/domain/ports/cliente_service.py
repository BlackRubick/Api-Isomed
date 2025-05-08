"""
Puerto para el servicio de clientes.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from app.domain.entities.cliente import Cliente


class ClienteService(ABC):
    """Interfaz para el servicio de clientes."""

    @abstractmethod
    def create_cliente(self, cliente_data: Dict[str, Any]) -> Cliente:
        """Crea un nuevo cliente."""
        pass

    @abstractmethod
    def get_cliente(self, cliente_id: int) -> Optional[Cliente]:
        """Obtiene un cliente por su ID."""
        pass

    @abstractmethod
    def get_all_clientes(self) -> List[Cliente]:
        """Obtiene todos los clientes."""
        pass

    @abstractmethod
    def update_cliente(self, cliente_id: int, cliente_data: Dict[str, Any]) -> Cliente:
        """Actualiza un cliente."""
        pass

    @abstractmethod
    def delete_cliente(self, cliente_id: int) -> bool:
        """Elimina un cliente."""
        pass