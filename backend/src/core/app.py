from fastapi import FastAPI

from routes import router
from core.services import lifespan


def create_app():
    app = FastAPI(title="App", 
          description="App description", 
          version="0.1.0", 
          docs_url="/api/docs",
          # openapi_url='/openapi.json'
          lifespan=lifespan
        )

    app.include_router(router, prefix="/api")

    return app

