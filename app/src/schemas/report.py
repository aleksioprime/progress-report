from pydantic import BaseModel, Field
from typing import Dict, List


class FeedbackRequest(BaseModel):
    """
    Модель запроса для генерации отзыва о студенте
    """
    name: str = Field(..., description="Имя студента")
    grades: Dict[str, int] = Field(..., description="Оценки студента по предметам, например: {'математика': 5, 'физика': 4}")
    achievements: List[str] = Field(..., description="Список достижений студента, например: ['Олимпиада по математике', 'Научная конференция']")


class ReportResponse(BaseModel):
    """
    Модель ответа с результатом генерации отзыва и расчетом стоимости
    """
    status: str = Field(..., description="Статус запроса (например, 'ok' или 'error')")
    result: str = Field(..., description="Сгенерированный отзыв о студенте")
    prompt_tokens: int = Field(..., description="Количество входных (запросных) токенов")
    completion_tokens: int = Field(..., description="Количество выходных (ответных) токенов")
    cost_usd: float = Field(..., description="Стоимость запроса в долларах США")
