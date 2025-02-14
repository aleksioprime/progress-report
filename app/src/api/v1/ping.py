import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from redis.asyncio import Redis

from src.db.redis import get_redis
from src.dependencies.auth import get_current_user

router = APIRouter()
logger = logging.getLogger("uvicorn.access")


@router.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    """
    Эндпоинт для проверки работы web-сервера
    """
    # logger.disabled = True
    return {"status": "ok", "message": "Server is up and running"}


@router.get("/ping/redis", status_code=status.HTTP_200_OK)
async def redis_health_check(
    user: dict = Depends(get_current_user),
    redis: Redis = Depends(get_redis)):
    """
    Эндпоинт для проверки состояния Redis
    """
    try:
        if await redis.ping():
            return {"status": "ok", "message": "Redis is operational"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": f"Redis check failed: {str(e)}"},
        )