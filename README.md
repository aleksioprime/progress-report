Создание среды на Python 3.9.4

```
pyenv pyenv virtualenv 3.9 report
pyenv activate report
```

Установка библиотек
```
pip install --upgrade pip
```

Установить llama:

```
brew install cmake
```
```
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
mkdir build && cd build
cmake ..
cmake --build . --config Release
```

Запуск сервиса:
```
docker-compose -p report -f docker-compose.yaml up -d --build
```

```
curl \
  --request POST \
  --data '{"yandexPassportOauthToken":"<OAuth-токен>"}' \
  https://iam.api.cloud.yandex.net/iam/v1/tokens
```

[Guide for QWEN](https://www.alibabacloud.com/help/en/model-studio/developer-reference/use-qwen-by-calling-api?spm=a2c63.p38356.help-menu-2400256.d_3_3_0.4c256dc30jJG0l)
