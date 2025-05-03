"""
Middleware para autenticación.
"""
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.infrastructure.adapters.security.jwt_manager import JWTManager
from app.domain.exceptions import InvalidTokenException


class JWTBearer(HTTPBearer):
    """Middleware para validar tokens JWT."""

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.jwt_manager = JWTManager()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Esquema de autenticación inválido."
                )
            try:
                payload = self.jwt_manager.validate_token(credentials.credentials)
                return payload
            except InvalidTokenException:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido o expirado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Credenciales de autenticación no proporcionadas"
            )