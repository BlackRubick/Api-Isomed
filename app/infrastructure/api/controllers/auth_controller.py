"""
Controlador de autenticación para la API con logs de depuración.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.application.services.auth_service import AuthServiceImpl
from app.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException, InvalidTokenException
from app.infrastructure.adapters.persistence.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.adapters.security.jwt_manager import JWTManager
from app.infrastructure.db.database import get_db

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("auth_controller")


# Modelos de Pydantic para las solicitudes y respuestas
class UserRegistrationRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirmPassword: str
    hospital: str = ""
    position: str = ""


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    hospital: str = ""
    position: str = ""


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    token: str
    user: UserResponse


# Router
router = APIRouter(prefix="/api/auth", tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


# Dependencia para obtener el servicio de autenticación
def get_auth_service(db: Session = Depends(get_db)):
    jwt_manager = JWTManager()
    user_repository = SQLAlchemyUserRepository(db)
    return AuthServiceImpl(user_repository, jwt_manager)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(request: UserRegistrationRequest, req: Request, auth_service: AuthServiceImpl = Depends(get_auth_service)):
    """Registra un nuevo usuario."""
    try:
        # Log de la solicitud entrante
        body = await req.json()
        logger.info(f"Solicitud de registro recibida: {body}")

        # Validar que las contraseñas coincidan
        if request.password != request.confirmPassword:
            logger.warning("Las contraseñas no coinciden en la solicitud de registro")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Las contraseñas no coinciden"
            )

        # Log de datos de registro válidos
        logger.info(f"Datos de registro válidos para el email: {request.email}")

        user_data = request.dict(exclude={"confirmPassword"})
        logger.info(f"Intentando registrar usuario con email: {user_data['email']}")

        user = auth_service.register(user_data)
        logger.info(f"Usuario registrado exitosamente con ID: {user.id}")

        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            hospital=user.hospital,
            position=user.position
        )
    except UserAlreadyExistsException as e:
        logger.error(f"Error de usuario existente: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en el registro: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, req: Request, auth_service: AuthServiceImpl = Depends(get_auth_service)):
    """Inicia sesión de un usuario."""
    try:
        # Log de la solicitud entrante
        body = await req.json()
        logger.info(f"Solicitud de login recibida para email: {body.get('email', 'no proporcionado')}")

        result = auth_service.login(request.email, request.password)
        logger.info(f"Login exitoso para el usuario: {result.user.email}")

        return LoginResponse(
            token=result.token,
            user=UserResponse(
                id=result.user.id,
                name=result.user.name,
                email=result.user.email,
                hospital=result.user.hospital,
                position=result.user.position
            )
        )
    except InvalidCredentialsException as e:
        logger.warning(f"Intento de login fallido: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Error inesperado en el login: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno del servidor: {str(e)}"
        )


@router.get("/me", response_model=UserResponse)
def get_current_user(
    token: str = Depends(oauth2_scheme),
    auth_service: AuthServiceImpl = Depends(get_auth_service),
    db: Session = Depends(get_db)
):
    """Obtiene el usuario actual basado en el token."""
    try:
        payload = auth_service.validate_token(token)
        logger.info(f"Token validado para usuario_id: {payload.get('user_id')}")

        user_repository = SQLAlchemyUserRepository(db)
        user = user_repository.find_by_id(payload.get("user_id"))

        if not user:
            logger.warning(f"Usuario no encontrado con ID: {payload.get('user_id')}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )

        logger.info(f"Información de usuario recuperada para: {user.email}")
        return UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            hospital=user.hospital,
            position=user.position
        )
    except InvalidTokenException:
        logger.warning("Token inválido o expirado")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )