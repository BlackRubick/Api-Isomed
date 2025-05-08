import uvicorn
import ssl
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import null

from app.infrastructure.api.server import app
from app.infrastructure.config.settings import Settings
from app.infrastructure.api.middleware.auth_middleware import JWTBearer

settings = Settings()


# Agregamos una ruta de prueba para depuración
@app.get("/api/admin/test-usuarios")
async def test_get_usuarios(token_data=Depends(JWTBearer())):
    """Endpoint de prueba que devuelve usuarios de prueba para depuración."""
    # Este endpoint siempre retornará datos de prueba independientemente del token
    return [
        {
            "id": 1,
            "nombre_completo": "Usuario Real 1",
            "email": "usuario1@example.com",
            "numero_cliente": "R001",
            "id_cliente": 1
        },
        {
            "id": 2,
            "nombre_completo": "Usuario Real 2",
            "email": "usuario2@example.com",
            "numero_cliente": "R002",
            "id_cliente": 2
        },
        {
            "id": 3,
            "nombre_completo": "Usuario Real 3",
            "email": "usuario3@example.com",
            "numero_cliente": null,
            "id_cliente": null
        }
    ]


if __name__ == "__main__":
    # Configuración SSL
    try:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # Rutas a tus certificados (ajústalas según donde estén ubicados)
        cert_path = "/etc/letsencrypt/live/34.232.185.39/fullchain.pem"
        key_path = "/etc/letsencrypt/live/34.232.185.39/privkey.pem"
        ssl_context.load_cert_chain(cert_path, key_path)

        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            ssl=ssl_context,
            reload=settings.DEBUG
        )
    except Exception as e:
        print(f"Error al configurar SSL: {e}")
        print("Iniciando servidor sin SSL...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.DEBUG
        )