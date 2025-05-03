"""
Entidad de usuario en el dominio.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """Entidad de dominio que representa un usuario en el sistema."""
    id: Optional[int] = None
    name: str = ""
    email: str = ""
    password_hash: str = ""
    hospital: str = ""
    position: str = ""
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()