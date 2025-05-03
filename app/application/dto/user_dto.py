"""
DTOs para usuarios.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserRegistrationDto:
    """DTO para registro de usuario."""
    name: str
    email: str
    password: str
    hospital: Optional[str] = ""
    position: Optional[str] = ""


@dataclass
class UserResponseDto:
    """DTO para respuesta con datos de usuario."""
    id: int
    name: str
    email: str
    hospital: Optional[str] = ""
    position: Optional[str] = ""


@dataclass
class LoginRequestDto:
    """DTO para solicitud de login."""
    email: str
    password: str


@dataclass
class LoginResponseDto:
    """DTO para respuesta de login."""
    token: str
    user: UserResponseDto