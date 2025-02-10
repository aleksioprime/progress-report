from pydantic import BaseModel, Field
from typing import List, Optional


class ParameterSchema(BaseModel):
    """Схема параметра запроса"""
    title: str = Field(..., description="Название параметра")
    value: str = Field(..., description="Значение параметра")


class FeedbackRequest(BaseModel):
    """
    Модель запроса для генерации отзыва о студенте
    """
    context: str = Field(..., description="Контекст")
    parameters: Optional[List[ParameterSchema]] = Field(..., description="Набор параметров")


class ReportResponse(BaseModel):
    """
    Модель ответа с результатом генерации отзыва и расчетом стоимости
    """
    status: str = Field(..., description="Статус запроса (например, 'ok' или 'error')")
    result: str = Field(..., description="Сгенерированный отзыв о студенте")
    prompt_tokens: int = Field(..., description="Количество входных (запросных) токенов")
    completion_tokens: int = Field(..., description="Количество выходных (ответных) токенов")
    cost: float = Field(..., description="Стоимость запроса в долларах США")
    currency: str = Field(..., description="Валюта")