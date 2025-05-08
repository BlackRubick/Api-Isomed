"""
Controlador para administración con token fijo.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from app.domain.entities.user import Usuario
from app.infrastructure.adapters.persistence.sqlalchemy_user_repository import SQLAlchemyUsuarioRepository
from app.infrastructure.adapters.persistence.sqlalchemy_cliente_repository import SQLAlchemyClienteRepository
from app.infrastructure.db.database import get_db

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("admin_controller_fixed")

# Configurar token fijo para administrador
ADMIN_TOKEN = "admin_fixed_token_12345"


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


# Router
router = APIRouter(prefix="/api/admin-fixed", tags=["admin-fixed"])


# Función para verificar el token fijo de administrador
async def verify_admin_token(authorization: str = Header(None)):
    if not authorization:
        logger.warning("No se proporcionó token de autorización")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se proporcionó token de autorización"
        )

    # Verificar formato Bearer
    try:
        scheme, token = authorization.split()
        if scheme.lower() != 'bearer':
            logger.warning(f"Esquema de autorización inválido: {scheme}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Esquema de autorización inválido"
            )
    except ValueError:
        logger.warning("Formato de autorización inválido")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Formato de autorización inválido"
        )

    # Verificar si el token coincide con el token de administrador
    if token != ADMIN_TOKEN:
        logger.warning("Token de administrador inválido")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de administrador inválido"
        )

    logger.info("Token de administrador válido")
    return True


@router.get("/usuarios", response_model=List[UsuarioResponse])
async def get_all_usuarios(db: Session = Depends(get_db), is_admin: bool = Depends(verify_admin_token)):
    """Obtiene todos los usuarios para administración usando token fijo."""
    try:
        logger.info("Obteniendo lista de usuarios para administración")

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


@router.put("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def update_usuario(
        usuario_id: int,
        request: UsuarioUpdateRequest,
        db: Session = Depends(get_db),
        is_admin: bool = Depends(verify_admin_token)
):
    """Actualiza los datos de asignación de cliente de un usuario usando token fijo."""
    try:
        logger.info(f"Actualizando usuario {usuario_id}")

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

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar usuario {usuario_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/usuarios/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(
        usuario_id: int,
        db: Session = Depends(get_db),
        is_admin: bool = Depends(verify_admin_token)
):
    """Elimina un usuario usando token fijo."""
    try:
        logger.info(f"Eliminando usuario {usuario_id}")

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