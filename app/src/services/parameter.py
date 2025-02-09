from uuid import UUID

from src.repositories.parameter import ParameterRepository
from src.schemas.parameter import ParameterCreateSchema, ParameterUpdateSchema, ParameterSchema


class ParameterService:
    """
    Сервис для управления запросами генераций репортов
    """
    def __init__(self, repository: ParameterRepository):
        self.repository = repository

    async def get_by_request(self, request_id: UUID) -> list[ParameterSchema]:
        """
        Возвращает список параметров запросов по его ID
        """
        parameters = await self.repository.get_by_request(request_id)
        return parameters

    async def create(self, request_id: UUID, body: ParameterCreateSchema) -> ParameterSchema:
        """
        Создает новый параметр запроса
        """
        parameter = await self.repository.create(request_id, body)
        return parameter

    async def update(self, request_id: UUID, parameter_id: UUID, body: ParameterUpdateSchema) -> ParameterSchema:
        """
        Редактирует параметр запроса по его ID
        """
        parameter = await self.repository.update(request_id, parameter_id, body)
        return parameter

    async def delete(self, request_id: UUID, parameter_id: UUID) -> None:
        """
        Удаляет параметр запроса по его ID
        """
        await self.repository.delete(request_id, parameter_id)