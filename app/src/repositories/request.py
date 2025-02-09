from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from uuid import UUID
from typing import List, Optional

from src.models.request import Request, Rating
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
                .where(Request.author_id == user_id)
            )
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise RequestException("Ошибка получения запросов на генерации репортов", str(e))

    async def get_by_id(self, request_id: UUID) -> Optional[RequestDetailedSchema]:
        """
        Возвращает запрос по его ID
        """
        try:
            query = (
                select(Request)
                .outerjoin(Rating, Request.id == Rating.request_id)
                .options(
                    joinedload(Request.parameters),
                    joinedload(Request.comments),
                )
                .where(Request.id == request_id)
                .group_by(Request.id)
            )
            result = await self.session.execute(query)

            request = result.scalars().unique().one_or_none()

            if not request:
                raise NoResultFound(f"Запрос с ID {request_id} не найден")

            request, average_rating = request
            request.average_rating = average_rating
            return request
        except SQLAlchemyError as e:
            raise RequestException("Ошибка получения запроса на генерацию репорта", str(e))

    async def create(self, body: RequestCreateSchema) -> RequestSchema:
        """
        Создаёт новый запрос
        """
        try:
            new_request = Request(
                name=body.name,
                author_id=body.user_id,
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
