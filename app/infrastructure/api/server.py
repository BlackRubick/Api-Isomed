"""
Configuración del servidor FastAPI con CORS mejorado.
"""
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.domain.exceptions import DomainException
from app.infrastructure.api.controllers.auth_controller import router as auth_router
from app.infrastructure.config.settings import Settings
from app.infrastructure.db.database import Base, engine

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("server")

# Crear tablas en la base de datos
try:
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas de base de datos creadas o verificadas exitosamente")
except Exception as e:
    logger.error(f"Error al crear tablas en la base de datos: {str(e)}", exc_info=True)
    raise

# Configuración
settings = Settings()

# Aplicación FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="API para gestión de autenticación de usuarios de ISOMED",
    version="1.0.0",
)

# Configuración de CORS mejorada
app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["https://isomed.com.mx"],  # Dominio con HTTPS
=======
    allow_origins=[
        "https://isomed.com.mx",
        "http://54.161.137.230"
    ],
>>>>>>> c4459b64e00a22471025c3448f0600721f20f3de
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)
# Incluir routers
app.include_router(auth_router)


# Middleware para loguear solicitudes
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Solicitud entrante: {request.method} {request.url}")

    response = await call_next(request)

    logger.info(f"Respuesta saliente: {response.status_code}")
    return response


# Manejador de excepciones
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    """Manejador para excepciones de dominio."""
    logger.warning(f"Excepción de dominio: {str(exc)}")
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


# Ruta de salud
@app.get("/api/health")
def health_check():
    """Verificación de salud de la API."""
    logger.info("Verificación de salud solicitada")
    return {"status": "ok", "name": settings.APP_NAME}
