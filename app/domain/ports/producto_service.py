"""
Puerto para el servicio de productos.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from app.domain.entities.producto import Producto


class ProductoService(ABC):
    """Interfaz para el servicio de productos."""

    @abstractmethod
    def create_producto(self, producto_data: Dict[str, Any]) -> Producto:
        """Crea un nuevo producto."""
        pass

    @abstractmethod
    def get_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        pass

    @abstractmethod
    def get_all_productos(self) -> List[Producto]:
        """Obtiene todos los productos."""
        pass

    @abstractmethod
    def update_producto(self, producto_id: int, producto_data: Dict[str, Any]) -> Producto:
        """Actualiza un producto."""
        pass

    @abstractmethod
    def delete_producto(self, producto_id: int) -> bool:
        """Elimina un producto."""
        pass