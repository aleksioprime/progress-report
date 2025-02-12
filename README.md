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

Установите Docker-Compose:
```
sudo apt install docker-compose
```

Настройте SSH-доступ:
```
ssh-keygen -t ed25519 -C "deploy@server" -f ~/.ssh/deploy_key
cat ~/.ssh/deploy_key.pub
```
Добавьте ключ в `Deploy keys` в настройках репозитория

Создайте файл конфигурации:
```
nano ~/.ssh/config
```

Добавьте в файл настройки:
```
Host github.com
    IdentityFile ~/.ssh/deploy_key
    User git
```

Проверьте доступ:
```
ssh -T git@github.com
```

## Добавление бесплатного SSL-сертификата

Установите модуль CertBot:
```
sudo apt install certbot python3-certbot-nginx -y
```

Проверьте установку:
```
certbot --version
```

Временно остановите контейнер:
```
docker stop report-front
```

Запустите CertBot для получения сертификатов
```
sudo certbot --nginx -d repgen.ru -d www.repgen.ru
```

Добавляем в контейнер переменные:
```yaml
volumes:
      - /etc/letsencrypt/live/repgen.ru/fullchain.pem:/etc/nginx/ssl/fullchain.pem
      - /etc/letsencrypt/live/repgen.ru/privkey.pem:/etc/nginx/ssl/privkey.pem
      - /etc/letsencrypt/live/repgen.ru/chain.pem:/etc/nginx/ssl/chain.pem
      - /etc/nginx/custom/nginx.conf:/etc/nginx/conf.d/default.conf
```

Измените `/etc/nginx/custom/nginx.conf`:
```
server {
    listen 80;
    server_name repgen.ru www.repgen.ru;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name repgen.ru www.repgen.ru;

    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_trusted_certificate /etc/nginx/ssl/chain.pem;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://report-app:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    error_page 404 /index.html;
```

Добавьте автообновление сертификатов (каждые 90 дней). Для этого открываем crontab
```
sudo crontab -e
```

Добавьте строку:
```
0 3 * * * certbot renew --quiet && docker restart report-front
```