"""
Controlador para administración de usuarios.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from app.domain.entities.user import Usuario
from app.infrastructure.adapters.persistence.sqlalchemy_user_repository import SQLAlchemyUsuarioRepository
from app.infrastructure.adapters.persistence.sqlalchemy_cliente_repository import SQLAlchemyClienteRepository
from app.infrastructure.api.middleware.auth_middleware import JWTBearer
from app.infrastructure.db.database import get_db

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("admin_controller")


# Modelos de Pydantic
class UsuarioUpdateRequest(BaseModel):
    id_cliente: Optional[int] = None
    numero_cliente: Optional[str] = None


class UsuarioResponse(BaseModel):
    id: int
    nombre_completo: str
    email: str
    numero_cliente: Optional[str] = None
    id_cliente: Optional[int] = None


class ClienteResponse(BaseModel):
    id: int
    nombre: str


# Router con middleware de autenticación
router = APIRouter(prefix="/api/admin", tags=["admin"])


# Verificar si el usuario es admin
async def verify_is_admin(token_data=Depends(JWTBearer())):
    """Verifica si el usuario es admin."""
    # Lógica simple: asumimos que hay una forma de identificar administradores
    # En este caso, por ejemplo, podríamos verificar el email o un campo role
    # En este ejemplo asumimos que el campo 'email' puede identificar al admin

    if 'email' in token_data and token_data['email'] == 'admin@hotmail.com':
        return token_data

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Se requieren privilegios de administrador"
    )


@router.get("/usuarios", response_model=List[UsuarioResponse], dependencies=[Depends(verify_is_admin)])
async def get_all_usuarios(db: Session = Depends(get_db)):
    """Obtiene todos los usuarios para administración."""
    try:
        usuario_repository = SQLAlchemyUsuarioRepository(db)
        usuarios = usuario_repository.find_all()

        logger.info(f"Retornando {len(usuarios)} usuarios para panel de administración")

        return [
            UsuarioResponse(
                id=usuario.id,
                nombre_completo=usuario.nombre_completo,
                email=usuario.email,
                numero_cliente=usuario.numero_cliente,
                id_cliente=usuario.id_cliente
            ) for usuario in usuarios
        ]
    except Exception as e:
        logger.error(f"Error al obtener usuarios para administración: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse, dependencies=[Depends(verify_is_admin)])
async def update_usuario(usuario_id: int, request: UsuarioUpdateRequest, db: Session = Depends(get_db)):
    """Actualiza los datos de asignación de cliente de un usuario."""
    try:
        usuario_repository = SQLAlchemyUsuarioRepository(db)

        # Buscar el usuario existente
        usuario = usuario_repository.find_by_id(usuario_id)
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )

        # Actualizar los campos relevantes
        usuario.id_cliente = request.id_cliente
        usuario.numero_cliente = request.numero_cliente

        # Guardar los cambios
        updated_usuario = usuario_repository.update(usuario)

        logger.info(f"Usuario {usuario_id} actualizado exitosamente")

        return UsuarioResponse(
            id=updated_usuario.id,
            nombre_completo=updated_usuario.nombre_completo,
            email=updated_usuario.email,
            numero_cliente=updated_usuario.numero_cliente,
            id_cliente=updated_usuario.id_cliente
        )

    except Exception as e:
        logger.error(f"Error al actualizar usuario {usuario_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT,
               dependencies=[Depends(verify_is_admin)])
async def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    """Elimina un usuario."""
    try:
        usuario_repository = SQLAlchemyUsuarioRepository(db)

        # Intentar eliminar
        result = usuario_repository.delete(usuario_id)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {usuario_id} no encontrado"
            )

        logger.info(f"Usuario {usuario_id} eliminado exitosamente")

        return None

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar usuario {usuario_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )