"""
Controlador para gestión de productos.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List, Optional

from app.application.services.producto_service import ProductoServiceImpl
from app.domain.exceptions import DomainException
from app.infrastructure.adapters.persistence.sqlalchemy_producto_repository import SQLAlchemyProductoRepository
from app.infrastructure.api.middleware.auth_middleware import JWTBearer
from app.infrastructure.db.database import get_db

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("producto_controller")


# Modelos de Pydantic
class ProductoRequest(BaseModel):
    tipo: str
    descripcion: Optional[str] = None
    precio: float


class ProductoResponse(BaseModel):
    id: int
    tipo: str
    descripcion: Optional[str] = None
    precio: float


# Router
router = APIRouter(prefix="/api/productos", tags=["productos"])


# Dependencia para obtener el servicio de productos
def get_producto_service(db: Session = Depends(get_db)):
    producto_repository = SQLAlchemyProductoRepository(db)
    return ProductoServiceImpl(producto_repository)


@router.post("", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(JWTBearer())])
async def create_producto(request: ProductoRequest, req: Request,
                          producto_service: ProductoServiceImpl = Depends(get_producto_service)):
    """Crea un nuevo producto."""
    try:
        # Log de la solicitud entrante
        body = await req.json()
        logger.info(f"Solicitud de creación de producto recibida: {body}")

        producto_data = {
            "tipo": request.tipo,
            "descripcion": request.descripcion,
            "precio": request.precio
        }
        producto = producto_service.create_producto(producto_data)

        logger.info(f"Producto creado exitosamente con ID: {producto.id}")

        return ProductoResponse(
            id=producto.id,
            tipo=producto.tipo,
            descripcion=producto.descripcion,
            precio=producto.precio
        )
    except DomainException as e:
        logger.error(f"Error de dominio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en la creación de producto: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("", response_model=List[ProductoResponse], dependencies=[Depends(JWTBearer())])
def get_all_productos(producto_service: ProductoServiceImpl = Depends(get_producto_service)):
    """Obtiene todos los productos."""
    try:
        productos = producto_service.get_all_productos()

        return [
            ProductoResponse(
                id=producto.id,
                tipo=producto.tipo,
                descripcion=producto.descripcion,
                precio=producto.precio
            ) for producto in productos
        ]
    except Exception as e:
        logger.error(f"Error inesperado al obtener productos: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/{producto_id}", response_model=ProductoResponse, dependencies=[Depends(JWTBearer())])
def get_producto(producto_id: int, producto_service: ProductoServiceImpl = Depends(get_producto_service)):
    """Obtiene un producto por su ID."""
    try:
        producto = producto_service.get_producto(producto_id)

        if not producto:
            logger.warning(f"Producto no encontrado con ID: {producto_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )

        return ProductoResponse(
            id=producto.id,
            tipo=producto.tipo,
            descripcion=producto.descripcion,
            precio=producto.precio
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al obtener producto: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put("/{producto_id}", response_model=ProductoResponse, dependencies=[Depends(JWTBearer())])
async def update_producto(producto_id: int, request: ProductoRequest, req: Request,
                          producto_service: ProductoServiceImpl = Depends(get_producto_service)):
    """Actualiza un producto existente."""
    try:
        # Log de la solicitud entrante
        body = await req.json()
        logger.info(f"Solicitud de actualización de producto recibida para ID {producto_id}: {body}")

        producto_data = {
            "tipo": request.tipo,
            "descripcion": request.descripcion,
            "precio": request.precio
        }
        producto = producto_service.update_producto(producto_id, producto_data)

        logger.info(f"Producto actualizado exitosamente con ID: {producto.id}")

        return ProductoResponse(
            id=producto.id,
            tipo=producto.tipo,
            descripcion=producto.descripcion,
            precio=producto.precio
        )
    except DomainException as e:
        logger.error(f"Error de dominio: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en la actualización de producto: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(JWTBearer())])
def delete_producto(producto_id: int, producto_service: ProductoServiceImpl = Depends(get_producto_service)):
    """Elimina un producto."""
    try:
        result = producto_service.delete_producto(producto_id)

        if not result:
            logger.warning(f"Producto no encontrado con ID: {producto_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Producto no encontrado"
            )

        logger.info(f"Producto eliminado exitosamente con ID: {producto_id}")

        return None
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error inesperado al eliminar producto: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )