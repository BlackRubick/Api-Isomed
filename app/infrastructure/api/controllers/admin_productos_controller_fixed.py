"""
Controlador para administración de productos con token fijo.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, OperationalError
from typing import List, Optional

from app.domain.entities.producto import Producto
from app.infrastructure.adapters.persistence.sqlalchemy_producto_repository import SQLAlchemyProductoRepository
from app.infrastructure.db.database import get_db

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("admin_productos_controller_fixed")

# Configurar token fijo para administrador
ADMIN_TOKEN = "admin_fixed_token_12345"

# Modelos de Pydantic
class ProductoRequestDto(BaseModel):
    tipo: str
    descripcion: Optional[str] = None
    precio: float


class ProductoResponseDto(BaseModel):
    id: int
    tipo: str
    descripcion: Optional[str] = None
    precio: float


# Router
router = APIRouter(prefix="/api/admin-fixed", tags=["admin-fixed-productos"])


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


@router.get("/productos", response_model=List[ProductoResponseDto])
async def get_all_productos(db: Session = Depends(get_db), is_admin: bool = Depends(verify_admin_token)):
    """Obtiene todos los productos para administración usando token fijo."""
    try:
        logger.info("Obteniendo lista de productos para administración")

        producto_repository = SQLAlchemyProductoRepository(db)
        productos = producto_repository.find_all()

        logger.info(f"Retornando {len(productos)} productos para panel de administración")

        return [
            ProductoResponseDto(
                id=producto.id,
                tipo=producto.tipo,
                descripcion=producto.descripcion,
                precio=producto.precio
            ) for producto in productos
        ]
    except Exception as e:
        logger.error(f"Error al obtener productos para administración: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post("/productos", response_model=ProductoResponseDto, status_code=status.HTTP_201_CREATED)
async def create_producto(
    request: ProductoRequestDto,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(verify_admin_token)
):
    """Crea un nuevo producto usando token fijo."""
    try:
        logger.info(f"Creando nuevo producto: {request.tipo}")

        producto_repository = SQLAlchemyProductoRepository(db)

        # Crear entidad de producto
        new_producto = Producto(
            tipo=request.tipo,
            descripcion=request.descripcion,
            precio=request.precio
        )

        # Guardar en repositorio
        created_producto = producto_repository.save(new_producto)

        logger.info(f"Producto creado exitosamente con ID: {created_producto.id}")

        return ProductoResponseDto(
            id=created_producto.id,
            tipo=created_producto.tipo,
            descripcion=created_producto.descripcion,
            precio=created_producto.precio
        )

    except Exception as e:
        logger.error(f"Error al crear producto: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.put("/productos/{producto_id}", response_model=ProductoResponseDto)
async def update_producto(
    producto_id: int,
    request: ProductoRequestDto,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(verify_admin_token)
):
    """Actualiza un producto existente usando token fijo."""
    try:
        logger.info(f"Actualizando producto {producto_id}")

        producto_repository = SQLAlchemyProductoRepository(db)

        # Buscar el producto existente
        producto = producto_repository.find_by_id(producto_id)
        if not producto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Producto con ID {producto_id} no encontrado"
            )

        # Actualizar los campos
        producto.tipo = request.tipo
        producto.descripcion = request.descripcion
        producto.precio = request.precio

        # Guardar los cambios
        updated_producto = producto_repository.update(producto)

        logger.info(f"Producto {producto_id} actualizado exitosamente")

        return ProductoResponseDto(
            id=updated_producto.id,
            tipo=updated_producto.tipo,
            descripcion=updated_producto.descripcion,
            precio=updated_producto.precio
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al actualizar producto {producto_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(verify_admin_token)
):
    """Elimina un producto usando token fijo."""
    try:
        logger.info(f"Eliminando producto {producto_id}")

        # Primero verificamos si hay órdenes asociadas a este producto
        from sqlalchemy import text
        check_query = text("""
            SELECT COUNT(*) as count FROM tableORDENDETRABAJO 
            WHERE idPRODUCTO_FK = :producto_id
        """)

        result = db.execute(check_query, {"producto_id": producto_id})
        orden_count = result.fetchone()[0]

        if orden_count > 0:
            logger.warning(f"No se puede eliminar el producto {producto_id} porque está siendo utilizado en {orden_count} órdenes de trabajo.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar el producto porque está siendo utilizado en {orden_count} órdenes de trabajo."
            )

        producto_repository = SQLAlchemyProductoRepository(db)

        # Intentar eliminar
        try:
            result = producto_repository.delete(producto_id)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Producto con ID {producto_id} no encontrado"
                )

            logger.info(f"Producto {producto_id} eliminado exitosamente")

            return None
        except IntegrityError as e:
            logger.error(f"Error de integridad al eliminar producto {producto_id}: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede eliminar el producto porque está siendo utilizado en otras partes del sistema."
            )
        except OperationalError as e:
            logger.error(f"Error operacional al eliminar producto {producto_id}: {str(e)}")
            db.rollback()

            # Intentar una alternativa más simple si hay problemas con la estructura de la tabla
            try:
                # Ejecutar SQL directo si necesitamos evitar SQLAlchemy
                query = text("DELETE FROM tablePRODUCTO WHERE idPRODUCTO = :id")
                db.execute(query, {"id": producto_id})
                db.commit()
                logger.info(f"Producto {producto_id} eliminado con SQL directo")
                return None
            except Exception as e2:
                db.rollback()
                logger.error(f"Error con SQL directo: {str(e2)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error interno del servidor: No se pudo eliminar el producto"
                )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error al eliminar producto {producto_id}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )