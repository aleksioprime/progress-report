from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.postgres import get_db_session
from src.services.comment import CommentService
from src.repositories.comment import CommentRepository


async def get_comment_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> CommentRepository:
    """
    Получает экземпляр CommentRepository с переданным AsyncSession (асинхронная сессия базы данных)
    """
    return CommentRepository(session)


def get_comment_service(
    repository: Annotated[CommentRepository, Depends(get_comment_repository)],
) -> CommentService:
    """
    Возвращает экземпляр CommentService с кешированием и репозиторием
    """
    return CommentService(repository=repository)