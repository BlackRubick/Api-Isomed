"""
Implementación del repositorio de usuarios con SQLAlchemy para MySQL.
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.domain.entities.user import User
from app.domain.ports.user_repository import UserRepository
from app.infrastructure.db.models import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """Implementación del repositorio de usuarios con SQLAlchemy."""

    def __init__(self, db: Session):
        self.db = db

    def _map_to_entity(self, model: UserModel) -> User:
        """Mapea un modelo a una entidad."""
        if model is None:
            return None

        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password_hash,
            hospital=model.hospital or "",
            position=model.position or "",
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _map_to_model(self, entity: User) -> UserModel:
        """Mapea una entidad a un modelo."""
        return UserModel(
            id=entity.id,
            name=entity.name,
            email=entity.email,
            password_hash=entity.password_hash,
            hospital=entity.hospital or "",
            position=entity.position or "",
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def save(self, user: User) -> User:
        """Guarda un usuario en el repositorio."""
        try:
            db_user = self._map_to_model(user)
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return self._map_to_entity(db_user)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"No se pudo guardar el usuario con email {user.email}, posiblemente ya existe.")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al guardar el usuario: {str(e)}")

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Busca un usuario por su ID."""
        try:
            db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            return self._map_to_entity(db_user)
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar usuario por ID: {str(e)}")

    def find_by_email(self, email: str) -> Optional[User]:
        """Busca un usuario por su email."""
        try:
            db_user = self.db.query(UserModel).filter(UserModel.email == email).first()
            return self._map_to_entity(db_user)
        except SQLAlchemyError as e:
            raise ValueError(f"Error al buscar usuario por email: {str(e)}")

    def find_all(self) -> List[User]:
        """Retorna todos los usuarios."""
        try:
            db_users = self.db.query(UserModel).all()
            return [self._map_to_entity(db_user) for db_user in db_users]
        except SQLAlchemyError as e:
            raise ValueError(f"Error al obtener todos los usuarios: {str(e)}")

    def delete(self, user_id: int) -> bool:
        """Elimina un usuario del repositorio."""
        try:
            db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
            if db_user:
                self.db.delete(db_user)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al eliminar usuario: {str(e)}")

    def update(self, user: User) -> User:
        """Actualiza un usuario en el repositorio."""
        try:
            db_user = self.db.query(UserModel).filter(UserModel.id == user.id).first()
            if not db_user:
                raise ValueError(f"Usuario con ID {user.id} no encontrado")

            # Actualizar campos
            db_user.name = user.name
            db_user.email = user.email
            db_user.password_hash = user.password_hash
            db_user.hospital = user.hospital
            db_user.position = user.position

            self.db.commit()
            self.db.refresh(db_user)
            return self._map_to_entity(db_user)
        except IntegrityError:
            self.db.rollback()
            raise ValueError(f"No se pudo actualizar el usuario con email {user.email}, quizás ya existe.")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise ValueError(f"Error al actualizar usuario: {str(e)}")