from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from uuid import UUID
from typing import List, Optional

from src.models.request import Comment
from src.schemas.comment import CommentSchema, CommentCreateSchema, CommentUpdateSchema
from src.exceptions.request import RequestException


class CommentRepository:
    """
    Репозиторий для работы с комментариями к запросам
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_request(self, request_id: UUID) -> List[CommentSchema]:
        """
        Возвращает список комментариев к запросу по его ID
        """
        try:
            query = (
                select(Comment)
                .where(Comment.request_id == request_id)
            )
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise RequestException("Ошибка получения комментариев к запросу", str(e))

    async def create(self, request_id: UUID, user_id: UUID, body: CommentCreateSchema) -> CommentSchema:
        """
        Создаёт новый комметарий к запросу
        """
        try:
            new_comment = Comment(
                request_id=request_id,
                user_id=user_id,
                text=body.text,
                )
            self.session.add(new_comment)
            await self.session.commit()
            await self.session.refresh(new_comment)
            return new_comment
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка создания комметария к запросу: {str(e)}")

    async def update(self, request_id: UUID, comment_id: UUID, body: CommentUpdateSchema) -> Optional[CommentSchema]:
        """
        Обновляет комментарий к запросу по его ID и ID запроса
        """
        update_data = {key: value for key, value in body.dict(exclude_unset=True).items()}
        if not update_data:
            raise NoResultFound(f"Нет данных для обновления")

        try:
            query = (
                update(Comment)
                .filter_by(id=comment_id, request_id=request_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            await self.session.execute(query)
            await self.session.commit()

            updated_comment = await self._get_by_id(comment_id)

            return updated_comment
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка редактирования комментария к запросу: {str(e)}")

    async def delete(self, request_id: UUID, comment_id: UUID) -> bool:
        """
        Удаляет комментарий к запросу по его ID и ID запроса
        """
        try:
            deleted_comment = await self._get_by_id(comment_id, request_id)

            await self.session.delete(deleted_comment)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка удаления комментария к запросу: {str(e)}")

    async def _get_by_id(self, comment_id: UUID, request_id: UUID = None) -> Comment:
        """
        Возвращает комментарий к запросу по его ID и ID запроса (если передан)
        """
        try:
            query = select(Comment).where(Comment.id == comment_id)

            if request_id:
                query = query.where(Comment.request_id == request_id)

            result = await self.session.execute(query)
            comment = result.scalars().unique().one_or_none()

            if not comment:
                raise NoResultFound(f"Комментарий с ID {comment_id} не найден")

            return comment
        except SQLAlchemyError as e:
            raise RequestException(f"Ошибка получения комментария к запросу: {str(e)}")
