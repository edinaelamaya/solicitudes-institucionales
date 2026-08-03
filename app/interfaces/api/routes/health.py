from fastapi import APIRouter, HTTPException, status

from app.infrastructure.database.session import check_database_connection
from app.infrastructure.settings.app_settings import get_settings

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str]:
    settings = get_settings()
    return {
        "status": "ok",
        "service": settings.app_name,
        "version": settings.app_version,
    }


@router.get("/health/ready")
def readiness_check() -> dict[str, str]:
    try:
        check_database_connection()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="service not ready",
        ) from exc

    return {"status": "ready"}
