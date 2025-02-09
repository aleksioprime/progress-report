from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_db_session
from src.services.request import RequestService
from src.repositories.request import RequestRepository


async def get_request_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> RequestRepository:
    """
    Получает экземпляр RequestRepository с переданным AsyncSession (асинхронная сессия базы данных)
    """
    return RequestRepository(session)


def get_request_service(
    repository: Annotated[RequestRepository, Depends(get_request_repository)],
) -> RequestService:
    """
    Возвращает экземпляр RequestService с кешированием и репозиторием
    """
    return RequestService(repository=repository)