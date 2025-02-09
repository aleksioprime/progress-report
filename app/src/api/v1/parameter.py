"""
Модуль с эндпоинтами для функций работы с параметрами запросов
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from src.dependencies.auth import get_current_user
from src.dependencies.parameter import get_parameter_service
from src.services.parameter import ParameterService
from src.schemas.parameter import ParameterCreateSchema, ParameterUpdateSchema, ParameterSchema


router = APIRouter()


@router.get(
    path='/requests/{request_id}/parameters',
    summary='Получить все параметры конкретного запроса',
    response_model=list[ParameterSchema],
    status_code=status.HTTP_200_OK,
)
async def get_parameter_by_request(
    request_id: UUID,
    service: Annotated[ParameterService, Depends(get_parameter_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> list[ParameterSchema]:
    """
    Возвращает список всех всех параметров по ID запроса
    """
    parameters = await service.get_by_request(request_id)
    return parameters


@router.post(
    path='/requests/{request_id}/parameters',
    summary='Создать параметр у запроса',
    response_model=ParameterSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_parameter(
    request_id: UUID,
    body: ParameterCreateSchema,
    service: Annotated[ParameterService, Depends(get_parameter_service)],
    user: Annotated[dict, Depends(get_current_user)],
) -> ParameterSchema:
    """
    Создаёт параметр для запроса по его ID
    """
    new_parameter = await service.create(request_id, body)
    return new_parameter


@router.patch(
    path='/requests/{request_id}/parameters/{parameter_id}',
    summary='Обновить параметр запроса',
    response_model=ParameterSchema,
    status_code=status.HTTP_200_OK,
)
async def update_parameter(
        request_id: UUID,
        parameter_id: UUID,
        body: ParameterUpdateSchema,
        service: Annotated[ParameterService, Depends(get_parameter_service)],
        user: Annotated[dict, Depends(get_current_user)],
) -> ParameterSchema:
    """
    Обновляет информацию о параметре по его ID
    """
    updated_parameter = await service.update(request_id, parameter_id, body)
    return updated_parameter


@router.delete(
    path='/requests/{request_id}/parameters/{parameter_id}',
    summary='Удалить параметр запроса',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_parameter(
        request_id: UUID,
        parameter_id: UUID,
        service: Annotated[ParameterService, Depends(get_parameter_service)],
        user: Annotated[dict, Depends(get_current_user)],
):
    """
    Удаляет параметр по его ID
    """
    await service.delete(request_id, parameter_id)
    return {"message": "Параметр успешно удалён"}