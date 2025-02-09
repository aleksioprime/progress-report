from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_db_session
from src.services.parameter import ParameterService
from src.repositories.parameter import ParameterRepository


async def get_parameter_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> ParameterRepository:
    """
    Получает экземпляр ParameterRepository с переданным AsyncSession (асинхронная сессия базы данных)
    """
    return ParameterRepository(session)


def get_parameter_service(
    repository: Annotated[ParameterRepository, Depends(get_parameter_repository)],
) -> ParameterService:
    """
    Возвращает экземпляр ParameterService с кешированием и репозиторием
    """
    return ParameterService(repository=repository)