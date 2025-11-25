from fastapi import FastAPI
from routers.api_router import api_router

# Main application factory
def create_app() -> FastAPI:
    app = FastAPI(
        title="MindScan Backend",
        version="2.0",
        description="MindScan diagnostic engine backend (SynMind)",
    )

    # Routers
    app.include_router(api_router)

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
