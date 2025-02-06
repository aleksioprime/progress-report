# Сервис для генерации репортов с помощью нейросетей

Сервис позволяет генерировать progress-репорты о студентах с использованием различных AI-моделей:

- Ollama (LLaMA 2 / Mistral)
- DeepSeek
- ChatGPT (OpenAI)
- Qwen
- YandexGPT

Сервис принимает данные о студенте и формирует краткий отзыв. Для работы используются API различных AI-провайдеров.

Документации по API провайдеров:

- [Документация по ollama](https://github.com/ollama/ollama)
- [Документация по ChatGPT API](https://platform.openai.com/docs/quickstart)
- [Документация по DeepSeek](https://api-docs.deepseek.com/)
- [Документация по QWEN API](https://www.alibabacloud.com/help/en/model-studio/developer-reference/use-qwen-by-calling-api)
- [Документация по YandexGPT API](https://yandex.cloud/ru/docs/foundation-models/quickstart/yandexgpt#sdk_1)


## Запуск сервиса

Скачайте репозиторий:
```
git clone https://github.com/aleksioprime/progress_reports.git
cd progress_reports
```

Или загрузите его архив:
```
wget https://github.com/aleksioprime/progress_reports/archive/refs/heads/main.zip
unzip main.zip
rm main.zip
cd progress_reports-main
```

Запустите сервис локально:
```
docker-compose -p report -f docker-compose.yaml up -d --build
```
