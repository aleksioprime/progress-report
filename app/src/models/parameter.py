import uuid

from sqlalchemy import (
    Column, String, ForeignKey, Text, Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres import Base


class UserProxy:
    """Прокси-класс для пользователя из внешнего сервиса"""

    def __init__(self, user_id: uuid.UUID):
        self.id = user_id


class ParameterSet(Base):
    __tablename__ = "parameter_sets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=True)
    author_id = Column(UUID(as_uuid=True), nullable=False)
    is_global = Column(Boolean, default=False)

    parameters = relationship("Parameter", back_populates="parameter_set")


class Parameter(Base):
    __tablename__ = "parameters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parameter_set_id = Column(UUID(as_uuid=True), ForeignKey("parameter_sets.id"), nullable=False)
    name = Column(String(100), nullable=False)
    value = Column(Text, nullable=False)

    parameter_set = relationship("ParameterSet", back_populates="parameters")
