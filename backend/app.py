from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Settings
from routers.api_router import api_router

# Load settings
settings = Settings()

# Application factory

def create_app() -> FastAPI:
    app = FastAPI(
        title="MindScan API",
        version="2.0",
        description="Core backend for MindScan (SynMind)",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(api_router)

    return app

# Export default app
app = create_app()