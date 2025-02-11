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
    path='/requests/user/{user_id}',
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
    path='/requests/me',
    summary='Получить все сохранённые запросы авторизированного пользователя',
    response_model=list[RequestSchema],
    status_code=status.HTTP_200_OK,
)
async def get_request_me(
    service: Annotated[RequestService, Depends(get_request_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> list[RequestSchema]:
    """
    Возвращает список всех запросов авторизированного пользователя
    """
    requests = await service.get_by_user(user.user_id)
    return requests

@router.get(
    path='/requests/global',
    summary='Получить общие запросы всех пользователей',
    response_model=list[RequestSchema],
    status_code=status.HTTP_200_OK,
)
async def get_request_global(
    service: Annotated[RequestService, Depends(get_request_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> list[RequestSchema]:
    """
    Возвращает список общих запросов всех пользователей
    """
    requests = await service.get_global()
    return requests

@router.get(
    path='/requests/{request_id}',
    summary='Получить запрос по его ID',
    response_model=RequestDetailedSchema,
    status_code=status.HTTP_200_OK,
)
async def get_request_by_id(
    request_id: UUID,
    service: Annotated[RequestService, Depends(get_request_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> RequestDetailedSchema:
    """
    Возвращает запрос пользователя по его ID
    """
    request = await service.get_by_id(request_id)
    return request

@router.post(
    path='/requests',
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
    new_request = await service.create(user.user_id, body)
    return new_request

@router.patch(
    path='/requests/{request_id}',
    summary='Обновить существующий запрос',
    response_model=RequestDetailedSchema,
    status_code=status.HTTP_200_OK,
)
async def update_request(
        request_id: UUID,
        body: RequestUpdateSchema,
        service: Annotated[RequestService, Depends(get_request_service)],
        user: Annotated[dict, Depends(get_current_user)],
) -> RequestDetailedSchema:
    """
    Обновляет информацию о запросе по его ID
    """
    updated_request = await service.update(request_id, body)
    return updated_request

@router.delete(
    path='/requests/{request_id}',
    summary='Удалить запрос',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_request(
        request_id: UUID,
        service: Annotated[RequestService, Depends(get_request_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    """
    Удаляет запрос по его ID
    """
    await service.delete(request_id)
    return {"message": "Запрос успешно удалён"}