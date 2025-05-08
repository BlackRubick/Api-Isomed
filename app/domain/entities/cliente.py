"""
Entidad de cliente en el dominio.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Cliente:
    """Entidad de dominio que representa un cliente en el sistema."""
    id: Optional[int] = None
    nombre: str = ""
    fecha_mov: Optional[datetime] = None

    def __post_init__(self):
        if self.fecha_mov is None:
            self.fecha_mov = datetime.utcnow()