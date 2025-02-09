from uuid import UUID

from src.repositories.request import RequestRepository
from src.schemas.request import RequestCreateSchema, RequestUpdateSchema, RequestSchema, RequestDetailedSchema


class RequestService:
    """
    Сервис для управления запросами генераций репортов
    """
    def __init__(self, repository: RequestRepository):
        self.repository = repository

    async def get_by_user(self, user_id: UUID) -> list[RequestSchema]:
        """
        Возвращает список запросов пользователя по его ID
        """
        requests = await self.repository.get_by_user(user_id)
        return requests

    async def get_by_id(self, request_id: UUID) -> RequestDetailedSchema:
        """
        Возвращает список запросов пользователя по его ID
        """
        requests = await self.repository.get_by_id(request_id)
        return requests

    async def create(self, body: RequestCreateSchema, user_id: UUID) -> RequestSchema:
        """
        Создает новый запрос
        """
        if not body.user_id:
            body.user_id = user_id

        request = await self.repository.create(body)
        return request

    async def update(self, request_id: UUID, body: RequestUpdateSchema) -> RequestSchema:
        """
        Редактирует запрос по его ID
        """
        return await self.repository.update(request_id, body)

    async def delete(self, request_id: UUID) -> None:
        """
        Удаляет запрос по его ID
        """
        await self.repository.delete(request_id)