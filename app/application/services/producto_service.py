"""
Implementación del servicio de productos.
"""
from typing import Dict, Any, Optional, List
from app.domain.ports.producto_service import ProductoService
from app.domain.ports.producto_repository import ProductoRepository
from app.domain.entities.producto import Producto


class ProductoServiceImpl(ProductoService):
    """Implementación del servicio de productos."""

    def __init__(self, producto_repository: ProductoRepository):
        self.producto_repository = producto_repository

    def create_producto(self, producto_data: Dict[str, Any]) -> Producto:
        """Crea un nuevo producto."""
        # Crear una nueva entidad de producto
        new_producto = Producto(
            tipo=producto_data["tipo"],
            descripcion=producto_data.get("descripcion", ""),
            precio=producto_data["precio"]
        )

        # Guardar el producto en el repositorio
        return self.producto_repository.save(new_producto)

    def get_producto(self, producto_id: int) -> Optional[Producto]:
        """Obtiene un producto por su ID."""
        return self.producto_repository.find_by_id(producto_id)

    def get_all_productos(self) -> List[Producto]:
        """Obtiene todos los productos."""
        return self.producto_repository.find_all()

    def update_producto(self, producto_id: int, producto_data: Dict[str, Any]) -> Producto:
        """Actualiza un producto."""
        # Buscar el producto existente
        existing_producto = self.producto_repository.find_by_id(producto_id)
        if not existing_producto:
            raise ValueError(f"Producto con ID {producto_id} no encontrado")

        # Actualizar los datos del producto
        existing_producto.tipo = producto_data["tipo"]
        existing_producto.descripcion = producto_data.get("descripcion", existing_producto.descripcion)
        existing_producto.precio = producto_data["precio"]

        # Guardar los cambios
        return self.producto_repository.update(existing_producto)

    def delete_producto(self, producto_id: int) -> bool:
        """Elimina un producto."""
        return self.producto_repository.delete(producto_id)