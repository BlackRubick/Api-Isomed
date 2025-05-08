"""
Implementación del repositorio de órdenes de trabajo con SQLAlchemy para MySQL.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.entities.orden_trabajo import OrdenDeTrabajo, LineaProducto
from app.domain.ports.orden_trabajo_repository import OrdenTrabajoRepository
from app.infrastructure.db.models import OrdenDeTrabajoModel


class SQLAlchemyOrdenTrabajoRepository(OrdenTrabajoRepository):
    """Implementación del repositorio de órdenes de trabajo con SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def _map_to_entity(self, model: OrdenDeTrabajoModel) -> OrdenDeTrabajo:
        """Mapea un modelo a una entidad."""
        if model is None:
            return None

        # Crear líneas de producto basadas en el modelo
        lineas_producto = []
        if model.idPRODUCTO_linea1 and model.cantidadPRODUCTO_linea1 and model.precio_unitarioPRODUCTO_linea1:
            linea1 = LineaProducto(
                id_producto=model.idPRODUCTO_linea1,
                cantidad=model.cantidadPRODUCTO_linea1,
                precio_unitario=model.precio_unitarioPRODUCTO_linea1
            )
            lineas_producto.append(linea1)

        # Aquí puedes agregar más líneas de producto si las tienes en tu modelo

        return OrdenDeTrabajo(
            id=model.idORDENDETRABAJO,
            id_cliente=model.idCLIENTE_FK,
            id_producto=model.idPRODUCTO_FK,
            status=model.statusORDENDETRABAJO,
            lineas_producto=lineas_producto
        )

    def _map_to_model(self, entity: OrdenDeTrabajo) -> OrdenDeTrabajoModel:
        """Mapea una entidad a un modelo."""
        model = OrdenDeTrabajoModel(
            idORDENDETRABAJO=entity.id,
            idCLIENTE_FK=entity.id_cliente,
            idPRODUCTO_FK=entity.id_producto,
            statusORDENDETRABAJO=entity.status
        )

        # Mapear líneas de producto
        if entity.lineas_producto and len(entity.lineas_producto) > 0:
            linea1 = entity.lineas_producto[0]
            model.idPRODUCTO_linea1 = linea1.id_producto
            model.cantidadPRODUCTO_linea1 = linea1.cantidad
            model.precio_unitarioPRODUCTO_linea1 = linea1.precio_unitario

        # Aquí puedes mapear más líneas si las necesitas

        return model

    def save(self, orden: OrdenDeTrabajo) -> OrdenDeTrabajo:
        """Guarda una orden de trabajo en el repositorio."""
        try:
            db_orden = self._map_to_model(orden)
            self.db.add(db_orden)
            self.db.commit()
            self.db.refresh(db_orden)
            return self._map_to_entity(db_orden)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al guardar la orden de trabajo: {str(e)}")

    def find_by_id(self, orden_id: int) -> Optional[OrdenDeTrabajo]:
        """Busca una orden de trabajo por su ID."""
        try:
            db_orden = self.db.query(OrdenDeTrabajoModel).filter(
                OrdenDeTrabajoModel.idORDENDETRABAJO == orden_id).first()
            return self._map_to_entity(db_orden)
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar orden de trabajo por ID: {str(e)}")

    def find_by_cliente_id(self, cliente_id: int) -> List[OrdenDeTrabajo]:
        """Busca órdenes de trabajo por ID de cliente."""
        try:
            db_ordenes = self.db.query(OrdenDeTrabajoModel).filter(OrdenDeTrabajoModel.idCLIENTE_FK == cliente_id).all()
            return [self._map_to_entity(db_orden) for db_orden in db_ordenes]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar órdenes de trabajo por cliente ID: {str(e)}")

    def find_by_status(self, status: str) -> List[OrdenDeTrabajo]:
        """Busca órdenes de trabajo por su estado."""
        try:
            db_ordenes = self.db.query(OrdenDeTrabajoModel).filter(
                OrdenDeTrabajoModel.statusORDENDETRABAJO == status).all()
            return [self._map_to_entity(db_orden) for db_orden in db_ordenes]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar órdenes de trabajo por estado: {str(e)}")

    def find_all(self) -> List[OrdenDeTrabajo]:
        """Retorna todas las órdenes de trabajo."""
        try:
            db_ordenes = self.db.query(OrdenDeTrabajoModel).all()
            return [self._map_to_entity(db_orden) for db_orden in db_ordenes]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al obtener todas las órdenes de trabajo: {str(e)}")

    def delete(self, orden_id: int) -> bool:
        """Elimina una orden de trabajo del repositorio."""
        try:
            db_orden = self.db.query(OrdenDeTrabajoModel).filter(
                OrdenDeTrabajoModel.idORDENDETRABAJO == orden_id).first()
            if db_orden:
                self.db.delete(db_orden)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al eliminar orden de trabajo: {str(e)}")

    def update(self, orden: OrdenDeTrabajo) -> OrdenDeTrabajo:
        """Actualiza una orden de trabajo en el repositorio."""
        try:
            db_orden = self.db.query(OrdenDeTrabajoModel).filter(
                OrdenDeTrabajoModel.idORDENDETRABAJO == orden.id).first()
            if not db_orden:
                raise ValueError(f"Orden de trabajo con ID {orden.id} no encontrada")

            db_orden.idCLIENTE_FK = orden.id_cliente
            db_orden.idPRODUCTO_FK = orden.id_producto
            db_orden.statusORDENDETRABAJO = orden.status

            # Actualizar líneas de producto
            if orden.lineas_producto and len(orden.lineas_producto) > 0:
                linea1 = orden.lineas_producto[0]
                db_orden.idPRODUCTO_linea1 = linea1.id_producto
                db_orden.cantidadPRODUCTO_linea1 = linea1.cantidad
                db_orden.precio_unitarioPRODUCTO_linea1 = linea1.precio_unitario

            # Aquí puedes actualizar más líneas si las tienes

            self.db.commit()
            self.db.refresh(db_orden)
            return self._map_to_entity(db_orden)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar orden de trabajo: {str(e)}")