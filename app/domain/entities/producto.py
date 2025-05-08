"""
Entidad de producto en el dominio.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Producto:
    """Entidad de dominio que representa un producto en el sistema."""
    id: Optional[int] = None
    tipo: str = ""
    descripcion: Optional[str] = ""
    precio: float = 0.0
    fecha_mov: Optional[datetime] = None

    def __post_init__(self):
        if self.fecha_mov is None:
            self.fecha_mov = datetime.utcnow()