"""
Implementación del repositorio de usuarios con SQLAlchemy para MySQL.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.entities.user import Usuario
from app.domain.ports.user_repository import UsuarioRepository
from app.infrastructure.db.models import UsuarioModel


class SQLAlchemyUsuarioRepository(UsuarioRepository):
    """Implementación del repositorio de usuarios con SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def _map_to_entity(self, model: UsuarioModel) -> Usuario:
        """Mapea un modelo a una entidad."""
        if model is None:
            return None

        return Usuario(
            id=model.idUSUARIO,
            nombre_completo=model.nombre_completoUSUARIO,
            email=model.emailUSUARIO,
            password_hash=model.passwordUSUARIO,
            numero_cliente=model.numero_clienteUSUARIO or "",
            id_cliente=model.idCLIENTE_FK,
            fecha_mov=model.fecha_movUSUARIO
        )

    def _map_to_model(self, entity: Usuario) -> UsuarioModel:
        """Mapea una entidad a un modelo."""
        return UsuarioModel(
            idUSUARIO=entity.id,
            nombre_completoUSUARIO=entity.nombre_completo,
            emailUSUARIO=entity.email,
            passwordUSUARIO=entity.password_hash,
            numero_clienteUSUARIO=entity.numero_cliente,
            idCLIENTE_FK=entity.id_cliente,
            fecha_movUSUARIO=entity.fecha_mov
        )

    def save(self, usuario: Usuario) -> Usuario:
        """Guarda un usuario en el repositorio."""
        try:
            db_usuario = self._map_to_model(usuario)
            self.db.add(db_usuario)
            self.db.commit()
            self.db.refresh(db_usuario)
            return self._map_to_entity(db_usuario)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"No se pudo guardar el usuario con email {usuario.email}, posiblemente ya existe.")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al guardar el usuario: {str(e)}")

    def find_by_id(self, usuario_id: int) -> Optional[Usuario]:
        """Busca un usuario por su ID."""
        try:
            db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUSUARIO == usuario_id).first()
            return self._map_to_entity(db_usuario)
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar usuario por ID: {str(e)}")

    def find_by_email(self, email: str) -> Optional[Usuario]:
        """Busca un usuario por su email."""
        try:
            db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.emailUSUARIO == email).first()
            return self._map_to_entity(db_usuario)
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar usuario por email: {str(e)}")

    def find_by_cliente_id(self, cliente_id: int) -> List[Usuario]:
        """Busca usuarios por ID de cliente."""
        try:
            db_usuarios = self.db.query(UsuarioModel).filter(UsuarioModel.idCLIENTE_FK == cliente_id).all()
            return [self._map_to_entity(db_usuario) for db_usuario in db_usuarios]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar usuarios por cliente ID: {str(e)}")

    def find_all(self) -> List[Usuario]:
        """Retorna todos los usuarios."""
        try:
            db_usuarios = self.db.query(UsuarioModel).all()
            return [self._map_to_entity(db_usuario) for db_usuario in db_usuarios]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al obtener todos los usuarios: {str(e)}")

    def delete(self, usuario_id: int) -> bool:
        """Elimina un usuario del repositorio."""
        try:
            db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUSUARIO == usuario_id).first()
            if db_usuario:
                self.db.delete(db_usuario)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al eliminar usuario: {str(e)}")

    def update(self, usuario: Usuario) -> Usuario:
        """Actualiza un usuario en el repositorio."""
        try:
            db_usuario = self.db.query(UsuarioModel).filter(UsuarioModel.idUSUARIO == usuario.id).first()
            if not db_usuario:
                raise ValueError(f"Usuario con ID {usuario.id} no encontrado")

            # Actualizar campos
            db_usuario.nombre_completoUSUARIO = usuario.nombre_completo
            db_usuario.emailUSUARIO = usuario.email
            db_usuario.passwordUSUARIO = usuario.password_hash
            db_usuario.numero_clienteUSUARIO = usuario.numero_cliente
            db_usuario.idCLIENTE_FK = usuario.id_cliente
            db_usuario.fecha_movUSUARIO = usuario.fecha_mov

            self.db.commit()
            self.db.refresh(db_usuario)
            return self._map_to_entity(db_usuario)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"No se pudo actualizar el usuario con email {usuario.email}, quizás ya existe.")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar usuario: {str(e)}")