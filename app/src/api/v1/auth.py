from fastapi import Depends, Query, APIRouter
from pydantic import BaseModel

from src.services.auth import AuthService
from src.dependencies.auth import get_auth_service


router = APIRouter()


class CodeRequest(BaseModel):
    code: str

@router.post(
    path="/auth/exchange_code",
    summary="Обменять code на access_token",
    )
async def exchange_code_for_token(
    code_request: CodeRequest,
    service: AuthService = Depends(get_auth_service),
    ):
    """
    Обмен кода авторизации на access_token через FastAPI
    """
    result = await service.exchange_code(code_request.code)
    return result
