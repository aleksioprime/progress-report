import uuid
from uuid import UUID
from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.request import Request, Parameter
from src.models.rating import Rating
from src.schemas.request import RequestSchema, RequestCreateSchema, RequestUpdateSchema, RequestDetailedSchema, ParameterSchema
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

    async def get_global(self) -> List[RequestSchema]:
        """
        Возвращает список общих запросов всех пользователей
        """
        try:
            query = (
                select(Request)
                .where(Request.is_global == True)
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
        Обновляет запрос по его ID, включая параметры
        """
        update_data = {
            key: value for key, value in body.dict(exclude_unset=True).items()
            if key != "parameters"
        }

        if not update_data and not body.parameters:
            raise NoResultFound(f"Нет данных для обновления")

        try:
            # Обновляем сам Request
            if update_data:
                query = (
                    update(Request)
                    .filter_by(id=request_id)
                    .values(**update_data)
                    .execution_options(synchronize_session="fetch")
                )
                await self.session.execute(query)

            # Обновляем параметры запроса, если они переданы
            if hasattr(body, "parameters") and body.parameters is not None:
                await self._update_parameters(request_id, body.parameters)

            await self.session.commit()

            # Возвращаем обновленный объект
            updated_request = await self.get_by_id(request_id)
            return updated_request

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка редактирования запроса: {str(e)}")

    async def _update_parameters(self, request_id: UUID, new_parameters: list[ParameterSchema]):
        """
        Обновляет параметры запроса: редактирует, добавляет новые, удаляет отсутствующие.
        """
        try:
            # Получаем текущие параметры
            query = select(Parameter).where(Parameter.request_id == request_id)
            result = await self.session.execute(query)
            existing_parameters = {param.id: param for param in result.scalars().all()}  # Словарь {id: объект}

            # Обрабатываем новые параметры
            new_param_ids = set()
            for param_data in new_parameters:
                if param_data.id in existing_parameters:
                    # Обновляем существующий параметр
                    existing_parameters[param_data.id].title = param_data.title
                    existing_parameters[param_data.id].value = param_data.value
                else:
                    # Создаём новый параметр
                    new_param = Parameter(
                        id=uuid.uuid4(),
                        request_id=request_id,
                        title=param_data.title,
                        value=param_data.value,
                    )
                    self.session.add(new_param)
                new_param_ids.add(param_data.id)

            # Удаляем параметры, которые не переданы
            for param_id in existing_parameters.keys():
                if param_id not in new_param_ids:
                    await self.session.delete(existing_parameters[param_id])

        except SQLAlchemyError as e:
            raise RequestException(f"Ошибка обновления параметров: {str(e)}")

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
