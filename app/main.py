import uvicorn
from app.infrastructure.api.server import app
from app.infrastructure.config.settings import Settings

settings = Settings()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.DEBUG else False,
    )