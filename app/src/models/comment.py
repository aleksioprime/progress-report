import uuid
from datetime import datetime

from sqlalchemy import (
    Column, ForeignKey, Text, DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from src.db.postgres import Base


class Comment(Base):
    """Комментарии к запросу на генерацию репорта"""
    __tablename__ = "comment"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    request_id = Column(UUID(as_uuid=True), ForeignKey("request.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    request = relationship("Request", back_populates="comments")