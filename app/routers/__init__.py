from fastapi import FastAPI

from app.routers import start
from app.routers import stop
from app.routers import configure
from app.routers import messages
from app.routers import device


def include_routers(app: FastAPI) -> FastAPI:
    app.include_router(start.router)
    app.include_router(stop.router)
    app.include_router(configure.router)
    app.include_router(messages.router)
    app.include_router(device.router)
    return app
