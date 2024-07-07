# Backend

## Описание
Сервис для обработки архивов фотографий с фотоловушек. Представляет API для загрузки архива, скачивания результатов, фотографий и их просмотр. <br/>
Основные библиотеки: <br/>
- FastApi
- Asyncpg
- Miniopy-async
- SQLAlchemy
- PyTorch
- Ultralytics

## Запуск приложения

### Установка зависимостей
Для установки основных зависимостей воспользуйтесь командой
```bash
python -m venv .venv

#Linux
source .venv/bin/activate

#Windows
.venv/scripts/activate
```

### Запуск
Для запуска выполните команду
```bash
python .\src\main.py 
```

!!Очень важно. Для запуска приложения требуются веса нейронной сети. Их требуется положить туда, откуда запускается приложение, а также назвать `best.pt`, `best_classifier.pt`


## Запуск в Docker
Для запуска приложения можно использовать Docker (смотри [docker-compose.yaml](https://github.com/Malinnik/grozny-hack/blob/main/docker-compose.yaml))

### Для запуска через Docker Compose
```bash
docker compose up
```
