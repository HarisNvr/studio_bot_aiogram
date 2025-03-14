#  Бот-помощник для студии Eleni_Workshop 

## Ссылка на бота: https://t.me/Eleni_WS_Bot

## Что умеет?

**Перенаправлять на соц.сети, рассказывать о направлениях студии, информировать о ценах и раскладывать Таро.**

### Используемые технологии

[![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://pypi.org/project/aiogram/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-000000?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Alembic](https://img.shields.io/badge/Alembic-7D4698?style=for-the-badge&logo=alembic&logoColor=white)](https://alembic.sqlalchemy.org/)
[![PostgreSQL](https://img.shields.io/badge/postgresql-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

### Развернуть проект на удаленном сервере:

**Предполагается, что на вашей машине уже установлен Docker с плагином Docker-compose!**

Официальный гайд по установке: https://docs.docker.com/engine/install/

- Клонировать репозиторий и перейти в него:
```
git clone https://github.com/HarisNvr/studio_bot_aiogram.git
cd studio_bot_aiogram
```
- Настраиваем переменные окружения:
```
sudo nano .env
```
```
# ПРИМЕР ФАЙЛА .env (пустой шаблон в формате txt есть в корне проекта)

#Global Vars
ADMIN_IDS=123,456,789  # Telegram_ID администраторов, через запятую.

#BOT
BOT_TOKEN=abcdef123456  # Telegram_API_bot_token
MAINTENANCE_MODE=False/True  # Перевод бота в состояние тех.работ 

#Postgre_Stuff
POSTGRES_USER=username  # Имя пользователя для доступа к БД
DB_PASSWORD=pass  # Пароль для доступа к БД
POSTGRES_DB=database  # Имя БД
DB_HOST=localhost  # Хост БД. Для разработки через IDE по умолчанию равен "localhost"
# Для продакшена автоматически внутри docker-compose файла переопределяется как "postgres"
DB_PORT=5432  # Порт контейнера с БД
ENGINE_ECHO=True/False  # Вывод отладки БД в консоль
TZ=Europe/Moscow  # Тайм-зона, которая будет задана для БД

#Soc_Profiles
INSTAGRAM=https://instagram.com/yourprofile  # Ссылка на Instagram профиль
VK=https://vk.com/yourprofile  # Ссылка на VK профиль
TG_DM=https://t.me/yourusername  # Ссылка для прямого сообщения в Telegram
TG_CHANNEL=https://t.me/yourchannel  # Ссылка на Telegram канал
WA=https://wa.me/1234567890  # Ссылка для общения в WhatsApp
YA_DISK=https://disk.yandex.ru/yourdisk  # Ссылка на Яндекс.Диск
SUPPORT=https://support.yoursite.com  # Ссылка на страницу поддержки

#Some_stuff
ORG_NAME=ACME_CORP  # Название вашей организации
CHANNEL_ID=1234567890  # Telegram_ID вашего канала
```

- Запустить Docker compose (на сервере, в продакшене):
```
sudo docker compose up -d
```
- Запустить Docker compose (локально только БД, для разработки через IDE):
```
sudo docker compose -f .\docker-compose_dev.yml up -d
```
**Бот при запуске сам проверит актуальность схемы в БД и применит миграции, если необходимо.**
## Команды, вводимые через '/' в чате:

```
start - Запуск бота
help - Главное меню
studio - Подробнее о студии
mk - Выездные МК
shop - Наш магазин
soc_profiles - Наши профили в соц.сетях
clean - Очистить чат
```

## TO-DO LIST:
- Добавление сторонних функций для пользователей.
- Перевод на Dialog.
- Добавление Django админ панели.
- Интеграции с интересными API.