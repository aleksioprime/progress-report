from pydantic import BaseModel, Field
from uuid import UUID
from typing import List


class UserSchema(BaseModel):
    """
    Pydantic-схема для пользователя, полученного через SkolStream API
    """
    user_id: UUID = Field(..., description="ID пользователя")
    email: str = Field(..., description="Email пользователя")
    roles: List[str] = Field(..., description="Роли пользователя")