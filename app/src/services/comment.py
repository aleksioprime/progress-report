from uuid import UUID

from src.repositories.comment import CommentRepository
from src.schemas.comment import CommentCreateSchema, CommentUpdateSchema, CommentSchema


class CommentService:
    """
    Сервис для управления запросами генераций репортов
    """
    def __init__(self, repository: CommentRepository):
        self.repository = repository

    async def get_by_request(self, request_id: UUID) -> list[CommentSchema]:
        """
        Возвращает список комментариев к запросу по его ID
        """
        comments = await self.repository.get_by_request(request_id)
        return comments

    async def create(self, request_id: UUID, user_id: UUID, body: CommentCreateSchema) -> CommentSchema:
        """
        Создает новый комментарий к запросу
        """
        comment = await self.repository.create(request_id, user_id, body)
        return comment

    async def update(self, request_id: UUID, comment_id: UUID, body: CommentUpdateSchema) -> CommentSchema:
        """
        Редактирует комментарий к запросу по его ID
        """
        comment = await self.repository.update(request_id, comment_id, body)
        return comment

    async def delete(self, request_id: UUID, comment_id: UUID) -> None:
        """
        Удаляет комментарий к запросу по его ID
        """
        await self.repository.delete(request_id, comment_id)