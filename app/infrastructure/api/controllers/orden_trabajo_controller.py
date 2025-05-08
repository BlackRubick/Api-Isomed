"""
Controlador para gestión de órdenes de trabajo.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from app.application.services.orden_trabajo_service import OrdenTrabajoServiceImpl
from app.domain.exceptions import DomainException
from app.infrastructure.adapters.persistence.sqlalchemy_orden_trabajo_repository import SQLAlchemyOrdenTrabajoRepository
from app.infrastructure.api.middleware.auth_middleware import JWTBearer
from app.infrastructure.db.database import get_db

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orden_trabajo_controller")


# Modelos de Pydantic
class LineaProductoRequest(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float


class OrdenTrabajoRequest(BaseModel):
    id_cliente: int
    id_producto: int
    status: str = "pendiente"
    lineas_producto: List[LineaProductoRequest]


class LineaProductoResponse(BaseModel):
    id_producto: int
    cantidad: int
    precio_unitario: float


class OrdenTrabajoResponse(BaseModel):
    id: int
    id_cliente: int
    id_producto: int
    status: str
    lineas_producto: List[LineaProductoResponse]


# Router
router = APIRouter(prefix="/api/ordenes", tags=["ordenes"])


# Dependencia para obtener el servicio de órdenes de trabajo
def get_orden_trabajo_service(db: Session = Depends(get_db)):
    orden_repository = SQLAlchemyOrdenTrabajoRepository(db)
    return OrdenTrabajoServiceImpl(orden_repository)


@router.post("", response_model=OrdenTrabajoResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(JWTBearer())])
async def create_orden(request: OrdenTrabajoRequest, req: Request,
                       orden_service: OrdenTrabajoServiceImpl = Depends(get_orden_trabajo_service)):
    """Crea una nueva orden de trabajo."""
    try:
        # Log de la solicitud entrante
        body = await req.json()
        logger.info(f"Solicitud de creación de orden de trabajo recibida: {body}")

        orden_data = {
            "id_cliente": request.id_cliente,
            "id_producto": request.id_producto,
            "status": request.status,
            "lineas_producto": [
                {
                    "id_producto": linea.id_producto,
                    "cantidad": linea.cantidad,
                    "precio_unitario": linea.precio_unitario
                } for linea in request.lineas_producto
            ]
        }
        orden = orden_service.create_orden(orden_data)

        logger.info(f"Orden de trabajo creada exitosamente con ID: {orden.id}")

        return OrdenTrabajoResponse(
            id=orden.id,
            id_cliente=orden.id_cliente,
            id_producto=orden.id_producto,
            status=orden.status,
            lineas_producto=[
                LineaProductoResponse(
                    id_producto=linea.id_producto,
                    cantidad=linea.cantidad,
                    precio_unitario=linea.precio_unitario
                ) for linea in orden.lineas_producto
            ]
        )
    except DomainException as e:
        logger.error(f"Error de dominio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en la creación de orden de trabajo: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("", response_model=List[OrdenTrabajoResponse], dependencies=[Depends(JWTBearer())])
def get_all_ordenes(orden_service: OrdenTrabajoServiceImpl = Depends(get_orden_trabajo_service)):
    """Obtiene todas las órdenes de trabajo."""
    try:
        ordenes = orden_service.get_all_ordenes()

        return [
            OrdenTrabajoResponse(
                id=orden.id,
                id_cliente=orden.id_cliente,
                id_producto=orden.id_producto,
                status=orden.status,
                lineas_producto=[
                    LineaProductoResponse(
                        id_producto=linea.id_producto,
                        cantidad=linea.cantidad,
                        precio_unitario=linea.precio_unitario
                    ) for linea in orden.lineas_producto
                ]
            ) for orden in ordenes
        ]
    except Exception as e:
        logger.error(f"Error inesperado al obtener órdenes de trabajo: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/cliente/{cliente_id}", response_model=List[OrdenTrabajoResponse], dependencies=[Depends(JWTBearer())])
def get_ordenes_by_cliente(cliente_id: int,
                           orden_service: OrdenTrabajoServiceImpl = Depends(get_orden_trabajo_service)):
    """Obtiene todas las órdenes de trabajo de un cliente."""
    try:
        ordenes = orden_service.get_ordenes_by_cliente(cliente_id)

        return [
            OrdenTrabajoResponse(
                id=orden.id,
                id_cliente=orden.id_cliente,
                id_producto=orden.id_producto,
                status=orden.status,
                lineas_producto=[
                    LineaProductoResponse(
                        id_producto=linea.id_producto,
                        cantidad=linea.cantidad,
                        precio_unitario=linea.precio_unitario
                    ) for linea in orden.lineas_producto
                ]
            ) for orden in ordenes
        ]
    except Exception as e:
        logger.error(f"Error inesperado al obtener órdenes de trabajo por cliente: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/{orden_id}", response_model=OrdenTrabajoResponse, dependencies=[Depends(JWTBearer())])
def get_orden(orden_id: int, orden_service: OrdenTrabajoServiceImpl = Depends(get_orden_trabajo_service)):
    """Obtiene una orden de trabajo por su ID."""
    try:
        orden = orden_service.get_orden(orden_id)

        if not orden:
            logger.warning(f"Orden de trabajo no encontrada con ID: {orden_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden de trabajo no encontrada"
            )

        return OrdenTrabajoResponse(
            id=orden.id,
            id_cliente=orden.id_cliente,
            id_producto=orden.id_producto,
            status=orden.status,
            lineas_producto=[
                LineaProductoResponse(
                    id_producto=linea.id_producto,
                    cantidad=linea.cantidad,
                    precio_unitario=linea.precio_unitario
                ) for linea in orden.lineas_producto
            ]
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al obtener orden de trabajo: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put("/{orden_id}", response_model=OrdenTrabajoResponse, dependencies=[Depends(JWTBearer())])
async def update_orden(orden_id: int, request: OrdenTrabajoRequest, req: Request,
                       orden_service: OrdenTrabajoServiceImpl = Depends(get_orden_trabajo_service)):
    """Actualiza una orden de trabajo existente."""
    try:
        # Log de la solicitud entrante
        body = await req.json()
        logger.info(f"Solicitud de actualización de orden de trabajo recibida para ID {orden_id}: {body}")

        orden_data = {
            "id_cliente": request.id_cliente,
            "id_producto": request.id_producto,
            "status": request.status,
            "lineas_producto": [
                {
                    "id_producto": linea.id_producto,
                    "cantidad": linea.cantidad,
                    "precio_unitario": linea.precio_unitario
                } for linea in request.lineas_producto
            ]
        }
        orden = orden_service.update_orden(orden_id, orden_data)

        logger.info(f"Orden de trabajo actualizada exitosamente con ID: {orden.id}")

        return OrdenTrabajoResponse(
            id=orden.id,
            id_cliente=orden.id_cliente,
            id_producto=orden.id_producto,
            status=orden.status,
            lineas_producto=[
                LineaProductoResponse(
                    id_producto=linea.id_producto,
                    cantidad=linea.cantidad,
                    precio_unitario=linea.precio_unitario
                ) for linea in orden.lineas_producto
            ]
        )
    except DomainException as e:
        logger.error(f"Error de dominio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en la actualización de orden de trabajo: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/{orden_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())])
def delete_orden(orden_id: int, orden_service: OrdenTrabajoServiceImpl = Depends(get_orden_trabajo_service)):
    """Elimina una orden de trabajo."""
    try:
        result = orden_service.delete_orden(orden_id)

        if not result:
            logger.warning(f"Orden de trabajo no encontrada con ID: {orden_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Orden de trabajo no encontrada"
            )

        logger.info(f"Orden de trabajo eliminada exitosamente con ID: {orden_id}")

        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al eliminar orden de trabajo: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )