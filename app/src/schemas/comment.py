from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional


class CommentSchema(BaseModel):
    """Схема комментария к запросу"""
    id: UUID
    request_id: UUID = Field(..., description="Идентификатор запроса, к которому привязан комментарий")
    user_id: UUID = Field(..., description="Идентификатор пользователя, оставившего комментарий")
    text: str = Field(..., description="Текст комментария")
    created_at: datetime = Field(..., description="Дата и время создания комментария")


class CommentCreateSchema(BaseModel):
    """Схема создания комментария к запросу"""
    text: str = Field(..., description="Текст комментария")


class CommentUpdateSchema(BaseModel):
    """Схема обновления комментария к запросу"""
    text: str = Field(..., description="Текст комментария")