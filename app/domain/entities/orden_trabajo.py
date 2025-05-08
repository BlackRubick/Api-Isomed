"""
Entidad de orden de trabajo en el dominio.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List


@dataclass
class LineaProducto:
    """Entidad que representa una línea de producto en una orden de trabajo."""
    id_producto: int
    cantidad: int
    precio_unitario: float


@dataclass
class OrdenDeTrabajo:
    """Entidad de dominio que representa una orden de trabajo en el sistema."""
    id: Optional[int] = None
    id_cliente: int = 0
    id_producto: int = 0
    status: str = "pendiente"
    lineas_producto: List[LineaProducto] = field(default_factory=list)
    id_usuario: Optional[int] = None
    fecha_mov: Optional[datetime] = None

    def __post_init__(self):
        if self.fecha_mov is None:
            self.fecha_mov = datetime.utcnow()