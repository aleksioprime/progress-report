"""
Модуль с эндпоинтами для функций работы с комментариями к запросам
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.dependencies.auth import get_current_user
from src.dependencies.comment import get_comment_service
from src.services.comment import CommentService
from src.schemas.comment import CommentCreateSchema, CommentUpdateSchema, CommentSchema


router = APIRouter()


@router.get(
    path='/requests/{request_id}/comments',
    summary='Получить все комментарии конкретного запроса',
    response_model=list[CommentSchema],
    status_code=status.HTTP_200_OK,
)
async def get_comment_by_request(
    request_id: UUID,
    service: Annotated[CommentService, Depends(get_comment_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> list[CommentSchema]:
    """
    Возвращает список всех комментариев по ID запроса
    """
    comments = await service.get_by_request(request_id)
    return comments


@router.post(
    path='/requests/{request_id}/comments',
    summary='Создать комментарий к запросу',
    response_model=CommentSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    request_id: UUID,
    body: CommentCreateSchema,
    service: Annotated[CommentService, Depends(get_comment_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> CommentSchema:
    """
    Создаёт комментарий к запросу по его ID
    """
    new_comment = await service.create(request_id, user.user_id, body)
    return new_comment


@router.patch(
    path='/requests/{request_id}/comments/{comment_id}',
    summary='Обновить комментарий к запросу',
    response_model=CommentSchema,
    status_code=status.HTTP_200_OK,
)
async def update_comment(
        request_id: UUID,
        comment_id: UUID,
        body: CommentUpdateSchema,
        service: Annotated[CommentService, Depends(get_comment_service)],
        user: Annotated[dict, Depends(get_current_user)],
) -> CommentSchema:
    """
    Обновляет комментарий по его ID
    """
    updated_comment = await service.update(request_id, comment_id, body)
    return updated_comment


@router.delete(
    path='/requests/{request_id}/comments/{comment_id}',
    summary='Удалить комментарий к запросу',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
        request_id: UUID,
        comment_id: UUID,
        service: Annotated[CommentService, Depends(get_comment_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    """
    Удаляет комментарий по его ID
    """
    await service.delete(request_id, comment_id)
    return {"message": "Комментарий успешно удалён"}