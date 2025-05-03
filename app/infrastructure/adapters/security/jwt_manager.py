"""
Gestor de JWT para manejo de tokens.
"""
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import jwt  # asegúrate de tener instalado PyJWT, no pyjwt
from app.domain.exceptions import InvalidTokenException
from app.infrastructure.config.settings import Settings


class JWTManager:
    """Gestor de JWT para la autenticación."""

    def __init__(self):
        self.settings = Settings()
        self.secret_key = self.settings.SECRET_KEY
        self.algorithm = self.settings.JWT_ALGORITHM
        self.token_expire_minutes = self.settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def generate_token(self, data: Dict[str, Any]) -> str:
        """Genera un token JWT con los datos proporcionados."""
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.token_expire_minutes)
        to_encode.update({"exp": expire})

        # Usa PyJWT correctamente
        try:
            # Primer intento con PyJWT
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            # Si es un objeto bytes (versiones antiguas de PyJWT), conviértelo a string
            if isinstance(encoded_jwt, bytes):
                return encoded_jwt.decode('utf-8')
            return encoded_jwt
        except AttributeError:
            # Intentar con pyjwt si es necesario
            import PyJWT
            encoded_jwt = PyJWT.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            if isinstance(encoded_jwt, bytes):
                return encoded_jwt.decode('utf-8')
            return encoded_jwt

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Valida un token JWT y devuelve los datos decodificados."""
        try:
            # Intentar decodificar con PyJWT
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except Exception as e:
            try:
                # Intentar con pyjwt si el primero falla
                import PyJWT
                payload = PyJWT.decode(token, self.secret_key, algorithms=[self.algorithm])
                return payload
            except Exception:
                # Si ambos fallan, lanzar la excepción
                raise InvalidTokenException(f"Token inválido o expirado: {str(e)}")