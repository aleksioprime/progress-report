from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.services.auth import AuthService
from src.schemas.auth import UserSchema

http_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    auth_service: AuthService = Depends(AuthService),
) -> UserSchema:
    """
    Dependency для получения текущего пользователя через SkolStream API.
    """
    user_data = await auth_service.verify_jwt_token(credentials)
    return UserSchema(**user_data)


def get_auth_service() -> AuthService:
    """
    Возвращает экземпляр AuthService
    """
    return AuthService()