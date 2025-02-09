import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, ForeignKey, Text, Boolean, Integer, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres import Base
from src.models.comment import Comment
from src.models.rating import Rating


class UserProxy:
    """Прокси-класс для пользователя из внешнего сервиса"""

    def __init__(self, user_id: uuid.UUID):
        self.id = user_id


class Parameter(Base):
    """Параметры запроса на генерацию репорта"""
    __tablename__ = "parameter"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("request.id"), nullable=False)
    title = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)

    request = relationship("Request", back_populates="parameters")


class Request(Base):
    """Запрос на генерацию репорта"""
    __tablename__ = "request"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    is_global = Column(Boolean, default=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parameters = relationship(Parameter, back_populates="request", cascade="all, delete-orphan")
    comments = relationship(Comment, back_populates="request", cascade="all, delete-orphan")
    ratings = relationship(Rating, back_populates="request", cascade="all, delete-orphan")
