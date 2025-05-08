import uvicorn
import ssl
from app.infrastructure.api.server import app
from app.infrastructure.config.settings import Settings

settings = Settings()

if __name__ == "__main__":
    # Configuración SSL
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
