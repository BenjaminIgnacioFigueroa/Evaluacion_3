from fastapi import APIRouter
from schemas import HealthResponse
from database import engine

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/", response_model=HealthResponse)
def health_check():
    """Endpoint de health check"""
    return {
        "status": "healthy",
        "database_connected": engine is not None,
        "database_url_configured": engine is not None
    }
