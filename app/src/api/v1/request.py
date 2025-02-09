"""
Модуль с эндпоинтами для функций работы с запросами для генерации репортов
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.dependencies.request import get_request_service
from src.dependencies.auth import get_current_user
from src.services.request import RequestService
from src.schemas.request import RequestCreateSchema, RequestUpdateSchema, RequestSchema, RequestDetailedSchema

router = APIRouter()


@router.get(
    path='/request/user/{user_id}',
    summary='Получить все сохранённые запросы пользователя по его ID',
    response_model=list[RequestSchema],
    status_code=status.HTTP_200_OK,
)
async def get_request_by_user(
    user_id: UUID,
    service: Annotated[RequestService, Depends(get_request_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> list[RequestSchema]:
    """
    Возвращает список всех сохранённых запросов пользователя по его ID
    """
    requests = await service.get_by_user(user_id)
    return requests

@router.get(
    path='/request/me',
    summary='Получить все сохранённые запросы авторизированного пользователя',
    response_model=list[RequestSchema],
    status_code=status.HTTP_200_OK,
)
async def get_request_me(
    service: Annotated[RequestService, Depends(get_request_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> list[RequestSchema]:
    """
    Возвращает список всех покупок авторизированного пользователя
    """
    requests = await service.get_by_user(user.user_id)
    return requests

@router.post(
    path='/request',
    summary='Создать запрос',
    response_model=RequestSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_request(
    body: RequestCreateSchema,
    service: Annotated[RequestService, Depends(get_request_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> RequestSchema:
    """
    Создаёт запрос
    """
    new_request = await service.create(body, user.user_id)
    return new_request

@router.patch(
    path='/request/{request_id}',
    summary='Обновить существующий запрос',
    response_model=RequestSchema,
)
async def update_request(
        request_id: UUID,
        body: RequestUpdateSchema,
        service: Annotated[RequestService, Depends(get_request_service)],
        user: Annotated[dict, Depends(get_current_user)],
) -> RequestSchema:
    """
    Обновляет информацию подписке по её ID
    """
    updated_request = await service.update(request_id, body)
    return updated_request

@router.delete(
    path='/request/{request_id}',
    summary='Удалить покупку',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_request(
        request_id: UUID,
        service: Annotated[RequestService, Depends(get_request_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    """
    Удаляет покупку по её ID
    """
    await service.delete(request_id)
    return {"message": "Запрос успешно удалён"}