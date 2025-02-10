from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime
from typing import List, Optional


class ParameterSchema(BaseModel):
    """Схема параметра запроса"""
    id: Optional[UUID] = None
    title: str = Field(..., description="Название параметра")
    value: Optional[str] = Field(None, description="Значение параметра")


class CommentSchema(BaseModel):
    """Схема комментария к запросу"""
    id: UUID
    user_id: UUID = Field(..., description="ID автора комментария")
    text: str = Field(..., description="Текст комментария")
    created_at: datetime = Field(..., description="Дата создания комментария")


class RatingSchema(BaseModel):
    """Схема рейтинга запроса"""
    id: UUID
    user_id: UUID = Field(..., description="ID автора рейтинга")
    score: int = Field(..., ge=1, le=5, description="Оценка от 1 до 5")
    created_at: datetime = Field(..., description="Дата создания рейтинга")


class RequestCreateSchema(BaseModel):
    """Схема создания запроса"""
    name: str = Field(..., description="Название запроса")
    context: str = Field("Ты учитель и пишешь краткие и конструктивные отзывы о студентах", description="Контекст запроса")
    is_global: bool = Field(False, description="Глобальный ли запрос")


class RequestUpdateSchema(BaseModel):
    """Схема обновления запроса"""
    name: Optional[str] = Field(None, description="Название запроса")
    is_global: Optional[bool] = Field(None, description="Глобальный ли запрос")
    context: Optional[str] = Field(None, description="Контекст запроса")
    comment: Optional[str] = Field(None, description="Комментарий к запросу")
    parameters: Optional[List[ParameterSchema]] = None


class RequestSchema(BaseModel):
    """Схема отображения запроса"""
    id: UUID
    user_id: UUID = Field(..., description="ID пользователя")
    name: str = Field(..., description="Название запроса")
    context: str = Field(..., description="Контекст запроса")
    is_global: bool = Field(..., description="Глобальный ли запрос")


class RequestDetailedSchema(RequestSchema):
    """Детальная схема запроса с параметрами, комментариями и рейтингами"""
    parameters: List[ParameterSchema] = Field(..., description="Список параметров запроса")
    comments: List[CommentSchema] = Field(..., description="Список комментариев к запросу")
    average_rating: float = Field(0, description="Средний рейтинг запроса")

    class Config:
        """
        Примечание. Pydantic по умолчанию ожидает словари,
        поэтому использование from_attributes = True
        позволяет Pydantic автоматически преобразовать
        объект ORM в Pydantic-модель
        """
        from_attributes = True
