"""
DTOs para productos.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ProductoRequestDto:
    """DTO para solicitud de producto."""
    tipo: str
    descripcion: Optional[str] = None
    precio: float = 0.0


@dataclass
class ProductoResponseDto:
    """DTO para respuesta con datos de producto."""
    id: int
    tipo: str
    descripcion: Optional[str] = None
    precio: float = 0.0