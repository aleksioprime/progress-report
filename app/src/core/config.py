"""
Этот модуль содержит конфигурационные настройки для различных сервисов,
таких как база данных, Redis и JWT.
"""

from datetime import timedelta
from typing import List

from dotenv import load_dotenv
from pydantic import Field, validator
from pydantic_settings import BaseSettings

load_dotenv()


class DBSettings(BaseSettings):
    """
    Конфигурация для настроек базы данных
    """
    name: str = Field(alias='DB_NAME', default='report')
    user: str = Field(alias='DB_USER', default='admin')
    password: str = Field(alias='DB_PASSWORD', default='123qwe')
    host: str = Field(alias='DB_HOST', default='127.0.0.1')
    port: int = Field(alias='DB_PORT', default=5432)
    show_query: bool = Field(alias='SHOW_SQL_QUERY', default=False)

    @property
    def _base_url(self) -> str:
        """ Формирует базовый URL для подключения к базе данных """
        return f"{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    @property
    def dsn(self) -> str:
        """ Формирует DSN строку для подключения к базе данных с использованием asyncpg """
        return f"postgresql+asyncpg://{self._base_url}"

    @property
    def alembic_url(self) -> str:
        """ Формирует URL для Alembic миграций """
        return f"postgresql+asyncpg://{self._base_url}"


class RedisSettings(BaseSettings):
    """
    Конфигурация для настроек Redis
    """
    host: str = Field(alias='REDIS_HOST', default='127.0.0.1')
    port: int = Field(alias='REDIS_PORT', default=6379)


class SkolStreamSettings(BaseSettings):
    """
    Конфигурация для настроек сервиса SkolStream
    """
    base_url: str = Field(alias='SKOLSTREAM_BASE_URL', default='')
    client_id: str = Field(alias='CLIENT_ID', default='')
    client_secret: str = Field(alias='CLIENT_SECRET', default='')

    @property
    def verify_url(self):
        return f"{self.base_url}/api/token/verify/"

    @property
    def token_url(self):
        return f"{self.base_url}/o/token/"


class OllamaSettings(BaseSettings):
    """
    Конфигурация для настроек Qwen API
    """
    base_url: str = Field(alias='OLLAMA_BASE_URL', default='http://report-ollama:11434/api/generate')
    model: str = "tinyllama"


class DeepSeekSettings(BaseSettings):
    """
    Конфигурация для настроек DeepSeek API
    """
    api_key: str = Field(alias='DEEPSEEK_API_KEY', default='')
    base_url: str = Field(alias='DEEPSEEK_BASE_URL', default='https://api.deepseek.com')
    model: str = "deepseek-chat"
    currency: str = "usd"
    price_it_per_1m: float = 0.55
    price_ot_per_1m: float = 2.19


class ChatGPTSettings(BaseSettings):
    """
    Конфигурация для настроек ChatGPT API
    """
    api_key: str = Field(alias='CHATGPT_API_KEY', default='')
    model: str = "gpt-4o"
    currency: str = "usd"
    price_it_per_1m: float = 2.50
    price_ot_per_1m: float = 10.00


class QwenSettings(BaseSettings):
    """
    Конфигурация для настроек Qwen API
    """
    api_key: str = Field(alias='QWEN_API_KEY', default='')
    base_url: str = Field(alias='QWEN_BASE_URL', default='https://dashscope-intl.aliyuncs.com/compatible-mode/v1')
    model: str = "qwen-plus"
    currency: str = "usd"
    price_it_per_1m: float = 0.0016 * 1000
    price_ot_per_1m: float = 0.0064 * 1000


class YandexGPTSettings(BaseSettings):
    """
    Конфигурация для настроек YandexGPT API
    """
    api_key: str = Field(alias='YANDEX_API_KEY', default='')
    folder_id: str = Field(alias='YANDEX_FOLDER_ID', default='')
    model: str = "yandexgpt"
    currency: str = "rub"
    price_per_1k: float = 1.20
    unit_per_token: float = 6.00


class Settings(BaseSettings):
    project_name: str = "Progress Report Generator"
    project_description: str = "An application for generating structured progress reports for students."

    skolstream: SkolStreamSettings = SkolStreamSettings()
    ollama: OllamaSettings = OllamaSettings()
    deepseek: DeepSeekSettings = DeepSeekSettings()
    chatgpt: ChatGPTSettings = ChatGPTSettings()
    qwen: QwenSettings = QwenSettings()
    yandexgpt: YandexGPTSettings = YandexGPTSettings()
    redis: RedisSettings = RedisSettings()
    db: DBSettings = DBSettings()

    default_host: str = "0.0.0.0"
    default_port: int = 8000
    cors_allow_origins_str: str = Field(alias="CORS_ALLOW_ORIGINS", default="")

    @property
    def cors_allow_origins(self) -> List[str]:
        """Преобразует строку cors_allow_origins_str в список"""
        return [origin.strip() for origin in self.cors_allow_origins_str.split(",") if origin.strip()]


settings = Settings()
