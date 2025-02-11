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
docker-compose -p report up -d --build
```

```
docker-compose -p report -f docker-compose.yaml up -d --build
```

Если выходит ошибка `exec /usr/src/app/entrypoint.sh: permission denied`, то нужно вручную установить флаг выполнения для entrypoint.sh в локальной системе:
```
chmod +x app/entrypoint.sh
```

## Проверка таблиц БД

Посмотрите, какие таблицы созданы в базе данных (в контейнере postgres):
```
docker-compose -p report exec postgres bash -c "psql -h localhost -p 5432 -U admin -d skolstream -c '\dt'"
```

## Работа с миграциями БД

Каждый раз, когда происходит изменение модели (Base.metadata), нужно сгенерировать новую миграцию
```shell
alembic revision --autogenerate -m "описание изменений"
```

После создания миграции её нужно применить в БД (head означает "применить до последней миграции")
```shell
alembic upgrade head
```

Если нужно применить конкретную миграцию, можно указать её ID:
```shell
alembic upgrade <migration_id>
```

Если после upgrade что-то сломалось, можно откатить последнюю миграцию:
```shell
alembic downgrade -1
```

Чтобы откатить до конкретной версии, укажи её ID:
```shell
alembic downgrade <migration_id>
```

Если локально сервис развёрнут в контейнере, то необходимо выполнять миграции из Docker, например:
```shell
docker exec -it report-app alembic revision --autogenerate -m "init"
docker exec -it report-app alembic upgrade head
```

В продакшене миграции, которые были созданы локально, применяются автоматически после перезапуска сервиса (инструкция в entrypoint.sh)

## Разворачивание на сервере

Установите сервер с ОС Ubuntu 22.04

Выполните обновление пакетов:
```
sudo apt update && sudo apt upgrade -y
```

Установите GIT:
```
sudo apt install -y git
```

Установите Docker-Compose
```
sudo apt install docker-compose
```