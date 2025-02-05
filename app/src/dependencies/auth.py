from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from src.services.auth import AuthService

http_bearer = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    auth_service: AuthService = Depends(AuthService),
):
    """
    Dependency для получения текущего пользователя через SkolStream API.
    """
    return await auth_service.verify_jwt_token(credentials)