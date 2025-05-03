"""
Implementación del servicio de autenticación.
"""
from typing import Dict, Any, Optional
import bcrypt
from app.domain.ports.auth_service import AuthService
from app.domain.ports.user_repository import UserRepository
from app.domain.entities.user import User
from app.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.application.dto.user_dto import UserRegistrationDto, LoginResponseDto, UserResponseDto


class AuthServiceImpl(AuthService):
    """Implementación del servicio de autenticación."""

    def __init__(self, user_repository: UserRepository, jwt_manager):
        self.user_repository = user_repository
        self.jwt_manager = jwt_manager

    def register(self, user_data: Dict[str, Any]) -> User:
        """Registra un nuevo usuario."""
        # Comprobar si el usuario ya existe
        existing_user = self.user_repository.find_by_email(user_data["email"])
        if existing_user:
            raise UserAlreadyExistsException(f"Ya existe un usuario con el email {user_data['email']}")

        # Hash de la contraseña
        password_hash = bcrypt.hashpw(user_data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Crear una nueva entidad de usuario
        new_user = User(
            name=user_data["name"],
            email=user_data["email"],
            password_hash=password_hash,
            hospital=user_data.get("hospital", ""),
            position=user_data.get("position", "")
        )

        # Guardar el usuario en el repositorio
        return self.user_repository.save(new_user)

    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        """Autentica a un usuario y devuelve el token si es exitoso."""
        user = self.user_repository.find_by_email(email)
        if not user:
            raise InvalidCredentialsException("Credenciales inválidas")

        # Verificar contraseña
        if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            raise InvalidCredentialsException("Credenciales inválidas")

        # Generar token JWT
        token = self.jwt_manager.generate_token({"user_id": user.id, "email": user.email})

        # Preparar respuesta
        user_response = UserResponseDto(
            id=user.id,
            name=user.name,
            email=user.email,
            hospital=user.hospital,
            position=user.position
        )

        return LoginResponseDto(token=token, user=user_response)

    def validate_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Valida un token y devuelve la información del usuario."""
        return self.jwt_manager.validate_token(token)