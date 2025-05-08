"""
Controlador para gestión de clientes.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List

from app.application.services.cliente_service import ClienteServiceImpl
from app.domain.exceptions import DomainException
from app.infrastructure.adapters.persistence.sqlalchemy_cliente_repository import SQLAlchemyClienteRepository
from app.infrastructure.api.middleware.auth_middleware import JWTBearer
from app.infrastructure.db.database import get_db

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("cliente_controller")

# Modelos de Pydantic
class ClienteRequest(BaseModel):
    nombre: str

class ClienteResponse(BaseModel):
    id: int
    nombre: str

# Router
router = APIRouter(prefix="/api/clientes", tags=["clientes"])

# Dependencia para obtener el servicio de clientes
def get_cliente_service(db: Session = Depends(get_db)):
    cliente_repository = SQLAlchemyClienteRepository(db)
    return ClienteServiceImpl(cliente_repository)

@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def create_cliente(request: ClienteRequest, req: Request, cliente_service: ClienteServiceImpl = Depends(get_cliente_service)):
    """Crea un nuevo cliente."""
    try:
        # Log de la solicitud entrante
        body = await req.json()
        logger.info(f"Solicitud de creación de cliente recibida: {body}")

        cliente_data = {"nombre": request.nombre}
        cliente = cliente_service.create_cliente(cliente_data)

        logger.info(f"Cliente creado exitosamente con ID: {cliente.id}")

        return ClienteResponse(
            id=cliente.id,
            nombre=cliente.nombre
        )
    except DomainException as e:
        logger.error(f"Error de dominio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en la creación de cliente: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("", response_model=List[ClienteResponse], dependencies=[Depends(JWTBearer())])
def get_all_clientes(cliente_service: ClienteServiceImpl = Depends(get_cliente_service)):
    """Obtiene todos los clientes."""
    try:
        clientes = cliente_service.get_all_clientes()

        return [
            ClienteResponse(
                id=cliente.id,
                nombre=cliente.nombre
            ) for cliente in clientes
        ]
    except Exception as e:
        logger.error(f"Error inesperado al obtener clientes: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.get("/{cliente_id}", response_model=ClienteResponse, dependencies=[Depends(JWTBearer())])
def get_cliente(cliente_id: int, cliente_service: ClienteServiceImpl = Depends(get_cliente_service)):
    """Obtiene un cliente por su ID."""
    try:
        cliente = cliente_service.get_cliente(cliente_id)

        if not cliente:
            logger.warning(f"Cliente no encontrado con ID: {cliente_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )

        return ClienteResponse(
            id=cliente.id,
            nombre=cliente.nombre
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al obtener cliente: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.put("/{cliente_id}", response_model=ClienteResponse, dependencies=[Depends(JWTBearer())])
async def update_cliente(cliente_id: int, request: ClienteRequest, req: Request, cliente_service: ClienteServiceImpl = Depends(get_cliente_service)):
    """Actualiza un cliente existente."""
    try:
        # Log de la solicitud entrante
        body = await req.json()
        logger.info(f"Solicitud de actualización de cliente recibida para ID {cliente_id}: {body}")

        cliente_data = {"nombre": request.nombre}
        cliente = cliente_service.update_cliente(cliente_id, cliente_data)

        logger.info(f"Cliente actualizado exitosamente con ID: {cliente.id}")

        return ClienteResponse(
            id=cliente.id,
            nombre=cliente.nombre
        )
    except DomainException as e:
        logger.error(f"Error de dominio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en la actualización de cliente: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )

@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())])
def delete_cliente(cliente_id: int, cliente_service: ClienteServiceImpl = Depends(get_cliente_service)):
    """Elimina un cliente."""
    try:
        result = cliente_service.delete_cliente(cliente_id)

        if not result:
            logger.warning(f"Cliente no encontrado con ID: {cliente_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cliente no encontrado"
            )

        logger.info(f"Cliente eliminado exitosamente con ID: {cliente_id}")

        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al eliminar cliente: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )