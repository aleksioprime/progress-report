FROM --platform=linux/amd64 python:3.11.3-buster

WORKDIR /usr/src/app

# Настройки Python
ENV PYTHONPATH=/usr/src/app:$PYTHONPATH
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновляем и устанавливаем зависимости для сборки
RUN apt-get update && apt-get install -y \
    netcat tzdata cmake ninja-build build-essential \
    gcc g++ libstdc++-8-dev git curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем часовой пояс
ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Обновляем pip
RUN pip install --upgrade pip

# Копируем зависимости
COPY ./requirements.txt ./

# Устанавливаем зависимости, используя CMAKE_ARGS для llama-cpp-python
RUN CMAKE_ARGS="-DLLAMA_NATIVE=ON" pip install -r ./requirements.txt

# Копируем код проекта
COPY . .

# Запускаем контейнер
CMD sh entrypoint.sh
