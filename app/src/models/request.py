import uuid
from datetime import datetime

from sqlalchemy import (
    Column, String, ForeignKey, Text, Boolean, Integer, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres import Base


class UserProxy:
    """Прокси-класс для пользователя из внешнего сервиса"""

    def __init__(self, user_id: uuid.UUID):
        self.id = user_id


class Request(Base):
    """Запрос на генерацию репорта"""
    __tablename__ = "request"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    is_global = Column(Boolean, default=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    parameters = relationship("Parameter", back_populates="request", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="request", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="request", cascade="all, delete-orphan")


class Parameter(Base):
    """Параметры запроса на генерацию репорта"""
    __tablename__ = "parameter"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("request.id"), nullable=False)
    title = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)

    request = relationship("Request", back_populates="parameters")


class Comment(Base):
    """Комментарии к запросу на генерацию репорта"""
    __tablename__ = "comment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("request.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("Request", back_populates="comments")


class Rating(Base):
    """Рейтинг запроса на генерацию репорта"""
    __tablename__ = "rating"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("request.id"), nullable=False)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("Request", back_populates="ratings")