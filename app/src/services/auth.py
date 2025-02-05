import httpx
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.core.config import settings


class AuthService:
    """
    Сервис аутентификации для проверки JWT-токена через SkolStream API
    """

    def __init__(self):
        self.verify_url = settings.skolstream.verify_url

    async def verify_jwt_token(self, credentials: HTTPAuthorizationCredentials):
        """
        Проверяет JWT-токен через SkolStream API
        """
        token = credentials.credentials

        async with httpx.AsyncClient() as client:
            response = await client.post(self.verify_url, json={"token": token})

        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        return response.json()