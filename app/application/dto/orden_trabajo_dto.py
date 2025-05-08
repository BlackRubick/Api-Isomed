"""
DTOs para órdenes de trabajo.
"""
from dataclasses import dataclass, field
from typing import List


@dataclass
class LineaProductoDto:
    """DTO para línea de producto en una orden de trabajo."""
    id_producto: int
    cantidad: int
    precio_unitario: float


@dataclass
class OrdenTrabajoRequestDto:
    """DTO para solicitud de orden de trabajo."""
    id_cliente: int
    id_producto: int
    lineas_producto: List[LineaProductoDto]
    status: str = "pendiente"


@dataclass
class OrdenTrabajoResponseDto:
    """DTO para respuesta con datos de orden de trabajo."""
    id: int
    id_cliente: int
    id_producto: int
    status: str
    lineas_producto: List[LineaProductoDto]