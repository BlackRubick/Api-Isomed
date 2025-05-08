"""
Puerto para el repositorio de productos.
"""
from abc import ABC, abstractmethod
from typing import Optional, List
from app.domain.entities.producto import Producto


class ProductoRepository(ABC):
    """Interfaz para el repositorio de productos."""

    @abstractmethod
    def save(self, producto: Producto) -> Producto:
        """Guarda un producto en el repositorio."""
        pass

    @abstractmethod
    def find_by_id(self, producto_id: int) -> Optional[Producto]:
        """Busca un producto por su ID."""
        pass

    @abstractmethod
    def find_by_tipo(self, tipo: str) -> List[Producto]:
        """Busca productos por su tipo."""
        pass

    @abstractmethod
    def find_all(self) -> List[Producto]:
        """Retorna todos los productos."""
        pass

    @abstractmethod
    def delete(self, producto_id: int) -> bool:
        """Elimina un producto del repositorio."""
        pass

    @abstractmethod
    def update(self, producto: Producto) -> Producto:
        """Actualiza un producto en el repositorio."""
        pass