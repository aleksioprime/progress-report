from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError, NoResultFound
from uuid import UUID
from typing import List, Optional

from src.models.request import Parameter
from src.schemas.parameter import ParameterSchema, ParameterCreateSchema, ParameterUpdateSchema
from src.exceptions.request import RequestException


class ParameterRepository:
    """
    Репозиторий для работы с параметрами запросов
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_request(self, request_id: UUID) -> List[ParameterSchema]:
        """
        Возвращает список параметров запросов по его ID
        """
        try:
            query = (
                select(Parameter)
                .where(Parameter.request_id == request_id)
            )
            result = await self.session.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise RequestException("Ошибка получения параметров запроса", str(e))

    async def create(self, request_id: UUID, body: ParameterCreateSchema) -> ParameterSchema:
        """
        Создаёт новый параметр запроса
        """
        try:
            new_parameter = Parameter(
                request_id=request_id,
                title=body.title,
                value=body.value,
                )
            self.session.add(new_parameter)
            await self.session.commit()
            await self.session.refresh(new_parameter)
            return new_parameter
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка создания параметра запроса: {str(e)}")

    async def update(self, request_id: UUID, parameter_id: UUID, body: ParameterUpdateSchema) -> Optional[ParameterSchema]:
        """
        Обновляет параметр запроса по его ID и ID запроса
        """
        update_data = {key: value for key, value in body.dict(exclude_unset=True).items()}
        if not update_data:
            raise NoResultFound(f"Нет данных для обновления")

        try:
            query = (
                update(Parameter)
                .filter_by(id=parameter_id, request_id=request_id)
                .values(**update_data)
                .execution_options(synchronize_session="fetch")
            )
            await self.session.execute(query)
            await self.session.commit()

            updated_parameter = await self._get_by_id(parameter_id)

            return updated_parameter
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка редактирования параметра запроса: {str(e)}")

    async def delete(self, request_id: UUID, parameter_id: UUID) -> bool:
        """
        Удаляет параметр запрос по его ID и ID запроса
        """
        try:
            deleted_parameter = await self._get_by_id(parameter_id, request_id)

            await self.session.delete(deleted_parameter)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RequestException(f"Ошибка удаления запроса на генерацию репорта: {str(e)}")

    async def _get_by_id(self, parameter_id: UUID, request_id: UUID = None) -> Parameter:
        """
        Возвращает параметр запроса по его ID и ID запроса (если передан)
        """
        try:
            query = select(Parameter).where(Parameter.id == parameter_id)

            if request_id:
                query = query.where(Parameter.request_id == request_id)

            result = await self.session.execute(query)
            parameter = result.scalars().unique().one_or_none()

            if not parameter:
                raise NoResultFound(f"Параметр с ID {parameter_id} не найден")

            return parameter
        except SQLAlchemyError as e:
            raise RequestException(f"Ошибка получения параметра запроса: {str(e)}")
