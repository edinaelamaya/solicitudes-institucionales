from fastapi import FastAPI

from app.interfaces.api.exception_handlers import register_exception_handlers
from app.interfaces.api.routes.health import router as health_router
from app.interfaces.api.routes.requests import router as requests_router
from app.infrastructure.database.bootstrap import initialize_database
from app.infrastructure.logging.logging_config import configure_logging
from app.infrastructure.settings.app_settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    )
    configure_logging(settings.log_level, settings.backend_log_file_path)
    register_exception_handlers(app)

    @app.on_event("startup")
    def on_startup() -> None:
        initialize_database()

    app.include_router(health_router)
    app.include_router(requests_router, prefix=settings.api_v1_prefix)
    return app


app = create_app()
