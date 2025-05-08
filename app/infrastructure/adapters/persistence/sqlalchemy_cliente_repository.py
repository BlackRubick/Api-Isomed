"""
Implementación del repositorio de clientes con SQLAlchemy para MySQL.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.entities.cliente import Cliente
from app.domain.ports.cliente_repository import ClienteRepository
from app.infrastructure.db.models import ClienteModel


class SQLAlchemyClienteRepository(ClienteRepository):
    """Implementación del repositorio de clientes con SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def _map_to_entity(self, model: ClienteModel) -> Cliente:
        """Mapea un modelo a una entidad."""
        if model is None:
            return None

        return Cliente(
            id=model.idCLIENTE,
            nombre=model.nombreCLIENTE,
            fecha_mov=model.fecha_movCLIENTE
        )

    def _map_to_model(self, entity: Cliente) -> ClienteModel:
        """Mapea una entidad a un modelo."""
        return ClienteModel(
            idCLIENTE=entity.id,
            nombreCLIENTE=entity.nombre,
            fecha_movCLIENTE=entity.fecha_mov
        )

    def save(self, cliente: Cliente) -> Cliente:
        """Guarda un cliente en el repositorio."""
        try:
            db_cliente = self._map_to_model(cliente)
            self.db.add(db_cliente)
            self.db.commit()
            self.db.refresh(db_cliente)
            return self._map_to_entity(db_cliente)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"No se pudo guardar el cliente {cliente.nombre}, posiblemente ya existe.")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al guardar el cliente: {str(e)}")

    def find_by_id(self, cliente_id: int) -> Optional[Cliente]:
        """Busca un cliente por su ID."""
        try:
            db_cliente = self.db.query(ClienteModel).filter(ClienteModel.idCLIENTE == cliente_id).first()
            return self._map_to_entity(db_cliente)
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar cliente por ID: {str(e)}")

    def find_by_nombre(self, nombre: str) -> List[Cliente]:
        """Busca clientes por su nombre."""
        try:
            db_clientes = self.db.query(ClienteModel).filter(ClienteModel.nombreCLIENTE.like(f"%{nombre}%")).all()
            return [self._map_to_entity(db_cliente) for db_cliente in db_clientes]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar clientes por nombre: {str(e)}")

    def find_all(self) -> List[Cliente]:
        """Retorna todos los clientes."""
        try:
            db_clientes = self.db.query(ClienteModel).all()
            return [self._map_to_entity(db_cliente) for db_cliente in db_clientes]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al obtener todos los clientes: {str(e)}")

    def delete(self, cliente_id: int) -> bool:
        """Elimina un cliente del repositorio."""
        try:
            db_cliente = self.db.query(ClienteModel).filter(ClienteModel.idCLIENTE == cliente_id).first()
            if db_cliente:
                self.db.delete(db_cliente)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al eliminar cliente: {str(e)}")

    def update(self, cliente: Cliente) -> Cliente:
        """Actualiza un cliente en el repositorio."""
        try:
            db_cliente = self.db.query(ClienteModel).filter(ClienteModel.idCLIENTE == cliente.id).first()
            if not db_cliente:
                raise ValueError(f"Cliente con ID {cliente.id} no encontrado")

            db_cliente.nombreCLIENTE = cliente.nombre
            db_cliente.fecha_movCLIENTE = cliente.fecha_mov

            self.db.commit()
            self.db.refresh(db_cliente)
            return self._map_to_entity(db_cliente)
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar cliente: {str(e)}")