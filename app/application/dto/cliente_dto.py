"""
DTOs para clientes.
"""
from dataclasses import dataclass


@dataclass
class ClienteRequestDto:
    """DTO para solicitud de cliente."""
    nombre: str


@dataclass
class ClienteResponseDto:
    """DTO para respuesta con datos de cliente."""
    id: int
    nombre: str