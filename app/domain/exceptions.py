"""
Excepciones de dominio.
"""


class DomainException(Exception):
    """Excepción base para el dominio."""
    pass


class UserAlreadyExistsException(DomainException):
    """Se lanza cuando se intenta registrar un usuario con un email ya existente."""
    pass


class InvalidCredentialsException(DomainException):
    """Se lanza cuando las credenciales proporcionadas son inválidas."""
    pass


class InvalidTokenException(DomainException):
    """Se lanza cuando un token es inválido o ha expirado."""
    pass