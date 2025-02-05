import httpx
from fastapi import HTTPException
from openai import OpenAI

from src.core.config import settings
from src.schemas.report import FeedbackRequest, ReportResponse

class ReportService:
    """
    Сервис для генерации отчетов с использованием Ollama, DeepSeek, ChatGPT и Qwen.
    """

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def generate_report(self, feedback: FeedbackRequest, provider: str) -> ReportResponse:
        """
        Генерирует отчет с использованием разных моделей AI
        """
        prompt = (
            f"Напиши отзыв на русском языке о студенте в одном предложении:\n"
            f"Имя: {feedback.name}\n"
            f"Оценки: {feedback.grades}\n"
            f"Достижения: {feedback.achievements}"
        )

        if provider == "ollama":
            return await self._generate_ollama(prompt)

        elif provider in {"deepseek", "chatgpt", "qwen"}:
            return await self._generate_openai_model(prompt, provider)

        else:
            raise HTTPException(status_code=400, detail="Неподдерживаемый провайдер AI")

    async def _generate_ollama(self, prompt: str) -> ReportResponse:
        """
        Генерирует отчет с помощью Ollama (LLaMA 2 / Mistral)
        """
        try:
            response = await self.client.post(
                settings.ollama.base_url,
                json={"model": settings.ollama.model, "prompt": prompt, "stream": False},
                timeout=180.0
            )
            response.raise_for_status()
            result_text = response.json().get("response", "").strip()

            return ReportResponse(
                status="ok",
                result=result_text,
                prompt_tokens=0,
                completion_tokens=0,
                cost_usd=0.0,
                )

        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к Ollama: {str(e)}")

    async def _generate_openai_model(self, prompt: str, provider: str) -> ReportResponse:
        """
        Генерирует отчет с помощью DeepSeek, ChatGPT или Qwen и рассчитывает стоимость.
        """
        config = getattr(settings, provider)  # Достаем настройки из settings (например, settings.deepseek)
        client = OpenAI(api_key=config.api_key, base_url=getattr(config, "base_url", None))

        try:
            response = client.chat.completions.create(
                model=config.model,  # Используем модель из конфига, например, `deepseek-chat`
                messages=[
                    {"role": "system", "content": "Ты учитель и пишешь краткие и конструктивные отзывы о студентах."},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )

            # Проверяем, есть ли в ответе ошибки
            if not response.choices or not response.choices[0].message:
                raise HTTPException(status_code=500, detail=f"Ошибка: пустой ответ от {provider.capitalize()}")

            result_text = response.choices[0].message.content.strip()

            # Получаем статистику по токенам
            usage = response.usage
            if not usage:
                raise HTTPException(status_code=500, detail=f"Ошибка: не удалось получить статистику по токенам от {provider.capitalize()}")

            prompt_tokens = usage.prompt_tokens
            completion_tokens = usage.completion_tokens

            # Рассчитываем стоимость запроса через отдельную функцию
            cost = self._calculate_cost(prompt_tokens, completion_tokens, config.price_it_per_1m, config.price_ot_per_1m)

            return ReportResponse(
                status="ok",
                result=result_text,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost_usd=cost,
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к {provider.capitalize()}: {str(e)}")

    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int, price_it_per_1m: float, price_ot_per_1m: float) -> float:
        """
        Рассчитывает стоимость запроса на основе использованных токенов и цен провайдера
        """
        cost = (
            (prompt_tokens / 1_000_000) * price_it_per_1m +
            (completion_tokens / 1_000_000) * price_ot_per_1m
        )
        return round(cost, 6)
