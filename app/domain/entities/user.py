"""
Entidad de usuario en el dominio.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    """Entidad de dominio que representa un usuario en el sistema."""
    id: Optional[int] = None
    nombre_completo: str = ""
    email: str = ""
    password_hash: str = ""
    numero_cliente: Optional[str] = ""
    id_cliente: Optional[int] = None
    fecha_mov: Optional[datetime] = None

    def __post_init__(self):
        if self.fecha_mov is None:
            self.fecha_mov = datetime.utcnow()