"""
Модуль с эндпоинтами для функций генерации репортов
"""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from starlette import status

from src.dependencies.report import get_report_service
from src.dependencies.auth import get_current_user
from src.services.report import ReportService
from src.schemas.report import ReportResponse, FeedbackRequest

router = APIRouter()


@router.post(
    path="/generate/ollama",
    summary="Генерировать репорт",
    response_model=ReportResponse,
)
async def generate_report_ollama(
    feedback: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportService = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст репорта на основе входных данных
    """
    report = await service.generate_report(feedback, provider="ollama")
    return report


@router.post(
    path="/generate/deepseek",
    summary="Генерировать отчет с DeepSeek",
    response_model=ReportResponse,
)
async def generate_deepseek_report(
    feedback: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportResponse = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст отчета на основе входных данных
    """
    report = await service.generate_report(feedback, provider="deepseek")
    return report


@router.post(
    path="/generate/сhatgpt",
    summary="Генерировать отчет с ChatGPT",
    response_model=ReportResponse,
)
async def generate_chatgpt_report(
    feedback: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportResponse = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст отчета на основе входных данных
    """
    report = await service.generate_report(feedback, provider="chatgpt")
    return report


@router.post(
    path="/generate/qwen",
    summary="Генерировать отчет с QWEN",
    response_model=ReportResponse,
)
async def generate_qwen_report(
    feedback: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportResponse = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст отчета на основе входных данных
    """
    report = await service.generate_report(feedback, provider="qwen")
    return report