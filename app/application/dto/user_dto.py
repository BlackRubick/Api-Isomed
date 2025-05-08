"""
DTOs para usuarios.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class UsuarioRegistrationDto:
    """DTO para registro de usuario."""
    nombre_completo: str
    email: str
    password: str
    confirm_password: str
    numero_cliente: Optional[str] = ""
    id_cliente: Optional[int] = None


@dataclass
class UsuarioResponseDto:
    """DTO para respuesta con datos de usuario."""
    id: int
    nombre_completo: str
    email: str
    numero_cliente: Optional[str] = ""
    id_cliente: Optional[int] = None


@dataclass
class LoginRequestDto:
    """DTO para solicitud de login."""
    email: str
    password: str


@dataclass
class LoginResponseDto:
    """DTO para respuesta de login."""
    token: str
    user: UsuarioResponseDto