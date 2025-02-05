"""
Этот модуль содержит конфигурационные настройки для различных сервисов,
таких как база данных, Redis и JWT.
"""

from datetime import timedelta

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


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

    @property
    def verify_url(self):
        return f"{self.base_url}/api/token/verify/"

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
    price_it_per_1m: float = 0.55
    price_ot_per_1m: float = 2.19


class ChatGPTSettings(BaseSettings):
    """
    Конфигурация для настроек ChatGPT API
    """
    api_key: str = Field(alias='CHATGPT_API_KEY', default='')
    model: str = "gpt-4o"
    price_it_per_1m: float = 2.50
    price_ot_per_1m: float = 10.00


class QwenSettings(BaseSettings):
    """
    Конфигурация для настроек Qwen API
    """
    api_key: str = Field(alias='QWEN_API_KEY', default='')
    base_url: str = Field(alias='QWEN_BASE_URL', default='https://dashscope-intl.aliyuncs.com/compatible-mode/v1')
    model: str = "qwen-plus"
    price_it_per_1m: float = 0.0016 * 1000
    price_ot_per_1m: float = 0.0064 * 1000



class Settings(BaseSettings):
    project_name: str = "Progress Report Generator"
    project_description: str = "An application for generating structured progress reports for students."
    skolstream: SkolStreamSettings = SkolStreamSettings()
    ollama: OllamaSettings = OllamaSettings()
    deepseek: DeepSeekSettings = DeepSeekSettings()
    chatgpt: ChatGPTSettings = ChatGPTSettings()
    qwen: QwenSettings = QwenSettings()
    redis: RedisSettings = RedisSettings()
    default_host: str = "0.0.0.0"
    default_port: int = 8000


settings = Settings()
