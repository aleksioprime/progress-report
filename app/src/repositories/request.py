from uuid import UUID
from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.request import Request
from src.models.rating import Rating
from src.schemas.request import RequestSchema, RequestCreateSchema, RequestUpdateSchema, RequestDetailedSchema
from src.exceptions.request import RequestException


class RequestRepository:
    """
    Репозиторий для работы с запросами генерации репортов
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user(self, user_id: UUID) -> List[RequestSchema]:
        """
        Возвращает список запросов пользователя по его ID
        """
        try:
            query = (
                select(Request)
                .where(Request.user_id == user_id)
            )
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise RequestException("Ошибка получения запросов на генерации репортов", str(e))

    async def get_by_id(self, request_id: UUID) -> Optional[RequestDetailedSchema]:
        """
        Возвращает запрос по его ID с средним рейтингом.
        """
        try:
            query = (
                select(Request, func.coalesce(func.avg(Rating.score), 0).label("average_rating"))
                .outerjoin(Rating, Request.id == Rating.request_id)
                .options(
                    joinedload(Request.parameters),
                    joinedload(Request.comments),
                )
                .where(Request.id == request_id)
                .group_by(Request.id)
            )
            result = await self.session.execute(query)

            row = result.first()  # ✅ Теперь получаем tuple (Request, average_rating)

            if not row:
                raise NoResultFound(f"Запрос с ID {request_id} не найден")

            request, average_rating = row  # ✅ Теперь распаковка корректна
            request.average_rating = average_rating  # ✅ Добавляем рейтинг в объект

            return request
        except SQLAlchemyError as e:
            raise RequestException("Ошибка получения запроса на генерацию репорта", str(e))

    async def create(self, user_id: UUID, body: RequestCreateSchema) -> RequestSchema:
        """
        Создаёт новый запрос
        """
        try:
            new_request = Request(
                user_id=user_id,
                name=body.name,
                is_global=body.is_global,
                )
            self.session.add(new_request)
            await self.session.commit()
            await self.session.refresh(new_request)
            return new_request
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка создания запроса на генерацию репорта: {str(e)}")

    async def update(self, request_id: UUID, body: RequestUpdateSchema) -> Optional[RequestDetailedSchema]:
        """
        Обновляет запрос по его ID
        """
        update_data = {key: value for key, value in body.dict(exclude_unset=True).items()}
        if not update_data:
            raise NoResultFound(f"Нет данных для обновления")

        try:
            query = (
                update(Request)
                .filter_by(id=request_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            await self.session.execute(query)
            await self.session.commit()

            updated_request = await self.get_by_id(request_id)

            return updated_request
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка редактирования запроса на генерацию репорта: {str(e)}")

    async def delete(self, request_id: UUID) -> bool:
        """
        Удаляет запрос по его ID
        """
        try:
            query = select(Request).where(Request.id == request_id)
            result = await self.session.execute(query)
            request = result.scalars().unique().one_or_none()

            if not request:
                raise NoResultFound(f"Запрос с ID {request_id} не найден")

            await self.session.delete(request)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка удаления запроса на генерацию репорта: {str(e)}")
