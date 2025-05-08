"""
Implementación del repositorio de productos con SQLAlchemy para MySQL.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.entities.producto import Producto
from app.domain.ports.producto_repository import ProductoRepository
from app.infrastructure.db.models import ProductoModel


class SQLAlchemyProductoRepository(ProductoRepository):
    """Implementación del repositorio de productos con SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def _map_to_entity(self, model: ProductoModel) -> Producto:
        """Mapea un modelo a una entidad."""
        if model is None:
            return None

        return Producto(
            id=model.idPRODUCTO,
            tipo=model.tipoPRODUCTO,
            descripcion=model.descripcionPRODUCTO,
            precio=model.precioPRODUCTO,
            fecha_mov=model.fecha_movPRODUCTO
        )

    def _map_to_model(self, entity: Producto) -> ProductoModel:
        """Mapea una entidad a un modelo."""
        return ProductoModel(
            idPRODUCTO=entity.id,
            tipoPRODUCTO=entity.tipo,
            descripcionPRODUCTO=entity.descripcion,
            precioPRODUCTO=entity.precio,
            fecha_movPRODUCTO=entity.fecha_mov
        )

    def save(self, producto: Producto) -> Producto:
        """Guarda un producto en el repositorio."""
        try:
            db_producto = self._map_to_model(producto)
            self.db.add(db_producto)
            self.db.commit()
            self.db.refresh(db_producto)
            return self._map_to_entity(db_producto)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al guardar el producto: {str(e)}")

    def find_by_id(self, producto_id: int) -> Optional[Producto]:
        """Busca un producto por su ID."""
        try:
            db_producto = self.db.query(ProductoModel).filter(ProductoModel.idPRODUCTO == producto_id).first()
            return self._map_to_entity(db_producto)
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar producto por ID: {str(e)}")

    def find_by_tipo(self, tipo: str) -> List[Producto]:
        """Busca productos por su tipo."""
        try:
            db_productos = self.db.query(ProductoModel).filter(ProductoModel.tipoPRODUCTO == tipo).all()
            return [self._map_to_entity(db_producto) for db_producto in db_productos]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar productos por tipo: {str(e)}")

    def find_all(self) -> List[Producto]:
        """Retorna todos los productos."""
        try:
            db_productos = self.db.query(ProductoModel).all()
            return [self._map_to_entity(db_producto) for db_producto in db_productos]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al obtener todos los productos: {str(e)}")

    def delete(self, producto_id: int) -> bool:
        """Elimina un producto del repositorio."""
        try:
            db_producto = self.db.query(ProductoModel).filter(ProductoModel.idPRODUCTO == producto_id).first()
            if db_producto:
                self.db.delete(db_producto)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al eliminar producto: {str(e)}")

    def update(self, producto: Producto) -> Producto:
        """Actualiza un producto en el repositorio."""
        try:
            db_producto = self.db.query(ProductoModel).filter(ProductoModel.idPRODUCTO == producto.id).first()
            if not db_producto:
                raise ValueError(f"Producto con ID {producto.id} no encontrado")

            db_producto.tipoPRODUCTO = producto.tipo
            db_producto.descripcionPRODUCTO = producto.descripcion
            db_producto.precioPRODUCTO = producto.precio
            db_producto.fecha_movPRODUCTO = producto.fecha_mov

            self.db.commit()
            self.db.refresh(db_producto)
            return self._map_to_entity(db_producto)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar producto: {str(e)}")