import httpx
from fastapi import HTTPException
from openai import OpenAI
from yandex_cloud_ml_sdk import YCloudML

from src.core.config import settings
from src.schemas.report import FeedbackRequest, ReportResponse

class ReportService:
    """
    Сервис для генерации отчетов с использованием Ollama, DeepSeek, ChatGPT и Qwen.
    """

    def __init__(self):
        self.client = httpx.AsyncClient()

    async def generate_report(self, body: FeedbackRequest, provider: str) -> ReportResponse:
        """
        Генерирует отчет с использованием разных моделей AI
        """
        feedback = { 'context': body.context }
        feedback['prompt'] = "Используй информацию о студенте:\n"

        if body.parameters:
            for param in body.parameters:
                feedback['prompt']+= f"- {param.title}: {param.value}\n"

        if provider == "ollama":
            return await self._generate_ollama(feedback)

        elif provider in {"deepseek", "chatgpt", "qwen"}:
            return await self._generate_openai_model(feedback, provider)

        elif provider == "yandexgpt":
            return await self._generate_yandexgpt(feedback)

        else:
            raise HTTPException(status_code=400, detail="Неподдерживаемый провайдер AI")

    async def _generate_ollama(self, feedback: dict) -> ReportResponse:
        """
        Генерирует отчет с помощью Ollama (LLaMA 2 / Mistral)
        """
        try:
            response = await self.client.post(
                settings.ollama.base_url,
                json={"model": settings.ollama.model, "prompt": f"{feedback['context']}. {feedback['prompt']}", "stream": False},
                timeout=180.0
            )
            response.raise_for_status()
            result_text = response.json().get("response", "").strip()

            return ReportResponse(
                status="ok",
                result=result_text,
                prompt_tokens=0,
                completion_tokens=0,
                cost=0.0,
                currency='-'
                )

        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к Ollama: {str(e)}")

    async def _generate_openai_model(self, feedback: dict, provider: str) -> ReportResponse:
        """
        Генерирует отчет с помощью DeepSeek, ChatGPT или Qwen и рассчитывает стоимость.
        """
        config = getattr(settings, provider)

        if provider == "chatgpt":
            proxy_url = "http://bo7j4b8oet:3Xdfbzq542@195.26.226.75:52998"
            transport = httpx.HTTPTransport(proxy=proxy_url)
            http_client = httpx.Client(transport=transport)
        else:
            http_client = httpx.Client()


        client = OpenAI(
            api_key=config.api_key,
            base_url=getattr(config, "base_url", None),
            http_client=http_client
            )

        try:
            response = client.chat.completions.create(
                model=config.model,
                messages=[
                    {"role": "system", "content": feedback['context']},
                    {"role": "user", "content": feedback['prompt']},
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
                cost=cost,
                currency=config.currency
            )

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к {provider.capitalize()}: {str(e)}")

    async def _generate_yandexgpt(self, feedback: dict) -> ReportResponse:
        """
        Генерирует отчет с помощью YandexGPT и рассчитывает стоимость.
        """
        config = settings.yandexgpt
        sdk = YCloudML(folder_id=config.folder_id, auth=config.api_key)

        messages = [
            {"role": "system", "text": feedback['context']},
            {"role": "user", "text": feedback['prompt']},
        ]

        try:
            result = sdk.models.completions(config.model).configure(temperature=0.5).run(messages)

            if not result or not result[0].text:
                raise HTTPException(status_code=500, detail="Ошибка: пустой ответ от YandexGPT")

            response_text = result[0].text.strip()

            prompt_tokens = len(feedback['prompt'].split())
            completion_tokens = len(response_text.split())
            total_tokens = prompt_tokens + completion_tokens
            units = total_tokens * config.unit_per_token
            cost = (config.price_per_1k / 1000) * units

            return ReportResponse(
                status="ok",
                result=response_text,
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                cost=round(cost, 6),
                currency=config.currency
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Ошибка при запросе к YandexGPT: {str(e)}")

    def _calculate_cost(self, prompt_tokens: int, completion_tokens: int, price_it_per_1m: float, price_ot_per_1m: float) -> float:
        """
        Рассчитывает стоимость запроса на основе использованных токенов и цен провайдера
        """
        cost = (
            (prompt_tokens / 1_000_000) * price_it_per_1m +
            (completion_tokens / 1_000_000) * price_ot_per_1m
        )
        return round(cost, 6)
