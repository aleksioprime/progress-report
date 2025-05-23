"""
Модуль с эндпоинтами для функций генерации репортов
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.dependencies.report import get_report_service
from src.dependencies.auth import get_current_user
from src.services.report import ReportService
from src.schemas.report import ReportResponse, FeedbackRequest

router = APIRouter()


@router.post(
    path="/generate/ollama",
    summary="Генерировать репорт",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_report_ollama(
    body: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportService = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст репорта на основе входных данных
    """
    report = await service.generate_report(body, provider="ollama")
    return report


@router.post(
    path="/generate/deepseek",
    summary="Генерировать отчет с DeepSeek",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_deepseek_report(
    body: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportResponse = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст отчета на основе входных данных
    """
    report = await service.generate_report(body, provider="deepseek")
    return report


@router.post(
    path="/generate/сhatgpt",
    summary="Генерировать отчет с ChatGPT",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_chatgpt_report(
    body: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportResponse = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст отчета на основе входных данных
    """
    report = await service.generate_report(body, provider="chatgpt")
    return report


@router.post(
    path="/generate/qwen",
    summary="Генерировать отчет с QWEN",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_qwen_report(
    body: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportResponse = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст отчета на основе входных данных
    """
    report = await service.generate_report(body, provider="qwen")
    return report


@router.post(
    path="/generate/yandexgpt",
    summary="Генерировать отчет с YandexGPT",
    response_model=ReportResponse,
    status_code=status.HTTP_200_OK,
)
async def generate_qwen_report(
    body: FeedbackRequest,
    user: Annotated[dict, Depends(get_current_user)],
    service: ReportResponse = Depends(get_report_service),
) -> ReportResponse:
    """
    Возвращает сгенерированный текст отчета на основе входных данных
    """
    report = await service.generate_report(body, provider="yandexgpt")
    return report