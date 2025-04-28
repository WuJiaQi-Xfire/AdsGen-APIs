"""Health check endpoints"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.deps import get_db
from src.services.health_service import health_service

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Check health of all services
    
    Returns:
        dict: Health status of all services
    """
    return await health_service.check_all_services()
