from typing import Annotated
from functools import lru_cache
from fastapi import Depends

from src.core.config import settings
from src.services.report import ReportService


def get_report_service() -> ReportService:
    """
    Возвращает экземпляр ReportService с кешированием
    """
    return ReportService()