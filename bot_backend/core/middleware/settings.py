from os import getenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.types import BotCommand
from dotenv import load_dotenv
from pytz import timezone

load_dotenv()


def get_admin_ids() -> list[int]:
    """
    Fetches and returns a list of admin IDs from the environment variable
    'ADMIN_IDS'. The 'ADMIN_IDS' environment variable is expected to be a
    comma-separated string of numeric admin IDs, which are then converted
    to integers.

    :return: List of admin IDs as integers.
    """

    admin_ids = []
    for admin_id in (getenv('ADMIN_IDS').split(',')):
        admin_ids.append(int(admin_id))

    return admin_ids


BOT = Bot(
    token=getenv('BOT_TOKEN'),
    default=DefaultBotProperties(parse_mode='HTML')
)
'''
An instance of the Telegram bot initialized with the bot token 
retrieved from environment variables.
'''

DEL_TIME = 0.5
'''
Time interval (in seconds) between deleting an old message and 
sending a new one in the chat.
'''

ADMIN_IDS = get_admin_ids()
'''
A list of Telegram user IDs that have the privilege to access and execute 
special administrative functions.
'''

POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')
DB_HOST = getenv('DB_HOST')
TZ_STR = getenv('TZ')
TZ = timezone(TZ_STR)

DATABASE_URL = (
    f'postgresql+asyncpg://{POSTGRES_USER}:'
    f'{POSTGRES_PASSWORD}@{DB_HOST}/{POSTGRES_DB}'
)
ENGINE_ECHO = getenv('ENGINE_ECHO', '').lower() == 'true'
MAINTENANCE_MODE = getenv('MAINTENANCE_MODE', '').lower() == 'true'

INSTAGRAM = getenv('INSTAGRAM')
VK = getenv('VK')
TG_DM = getenv('TG_DM')
TG_CHANNEL = getenv('TG_CHANNEL')
WA = getenv('WA')
YA_DISK = getenv('YA_DISK')
SUPPORT = getenv('SUPPORT')
ORG_NAME = getenv('ORG_NAME')

CHANNEL_ID = int(getenv('CHANNEL_ID'))

COMMANDS = [
    BotCommand(
        command="start",
        description="Запуск бота"
    ),
    BotCommand(
        command="help",
        description="Главное меню"
    ),
    BotCommand(
        command="studio",
        description="Подробнее о студии"
    ),
    BotCommand(
        command="mk",
        description="Выездные МК"
    ),
    BotCommand(
        command="shop",
        description="Наш магазин"
    ),
    BotCommand(
        command="soc_profiles",
        description="Наши профили в соц.сетях"
    ),
    BotCommand(
        command="clean",
        description="Очистить чат"
    ),
]
