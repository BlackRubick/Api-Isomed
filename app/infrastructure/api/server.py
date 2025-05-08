"""
Configuración del servidor FastAPI con CORS mejorado.
"""
import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.domain.exceptions import DomainException
from app.infrastructure.api.controllers.auth_controller import router as auth_router
from app.infrastructure.api.controllers.cliente_controller import router as cliente_router
from app.infrastructure.api.controllers.producto_controller import router as producto_router
from app.infrastructure.api.controllers.orden_trabajo_controller import router as orden_trabajo_router
from app.infrastructure.api.controllers.admin_controller import router as admin_router
from app.infrastructure.api.controllers.admin_controller_fixed import router as admin_fixed_router
from app.infrastructure.api.controllers.admin_productos_controller_fixed import router as admin_productos_fixed_router  # Nuevo router
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
    description="API para gestión del sistema ISOMED",
    version="1.0.0",
)

# Configuración de CORS mejorada
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://isomed.com.mx",
        "http://54.161.137.230",
        "http://34.232.185.39:8000",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Incluir routers
app.include_router(auth_router)
app.include_router(cliente_router)
app.include_router(producto_router)
app.include_router(orden_trabajo_router)
app.include_router(admin_router)
app.include_router(admin_fixed_router)
app.include_router(admin_productos_fixed_router)  # Incluir el router de productos con token fijo


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