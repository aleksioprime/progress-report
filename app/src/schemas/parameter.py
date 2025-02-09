from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


class ParameterSchema(BaseModel):
    """Схема параметра запроса"""
    id: UUID
    title: str = Field(..., description="Название параметра")
    value: Optional[str] = Field(None, description="Значение параметра")


class ParameterCreateSchema(BaseModel):
    """Схема создания параметра запроса"""
    title: str = Field(..., description="Название параметра")
    value: Optional[str] = Field(None, description="Значение параметра")


class ParameterUpdateSchema(BaseModel):
    """Схема обновления параметра запроса"""
    title: Optional[str] = Field(None, description="Название параметра")
    value: Optional[str] = Field(None, description="Значение параметра")