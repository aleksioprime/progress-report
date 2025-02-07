import httpx
import json
import base64
import logging
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials

from src.core.config import settings

logger = logging.getLogger(__name__)

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

    async def exchange_code(self, code: str):
        """
        Обмен кода авторизации на access_token
        """
        credentials = base64.b64encode(f"{settings.skolstream.client_id}:{settings.skolstream.client_secret}".encode()).decode()

        url = "http://backend:8000/o/token/"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {credentials}",
        }
        data = {
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost:8234/callback",
            "code": code if isinstance(code, str) else str(code),  # Преобразуем в строку
        }

        # Логируем перед отправкой запроса
        logger.info(f"Отправка запроса на обмен кода авторизации:")
        logger.info(f"URL: {url}")
        logger.info(f"Headers: {headers}")  # Убираем json.dumps, т.к. это уже строка
        logger.info(f"Data: {data}")  # Словарь можно логировать без json.dumps

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, data=data)

            # Логируем ответ
            logger.info(f"Ответ от сервера: статус {response.status_code}")
            logger.info(f"Тело ответа: {response.text}")

            try:
                response_json = response.json()
            except json.decoder.JSONDecodeError:
                logger.error("Ошибка декодирования JSON в ответе")
                raise HTTPException(status_code=500, detail="Ошибка декодирования JSON")

            if response.status_code != 200:
                logger.warning(f"Ошибка при получении токена: {response_json}")
                raise HTTPException(status_code=response.status_code, detail=response_json)

            return response_json
