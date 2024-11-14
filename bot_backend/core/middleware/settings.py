from os import getenv
from pathlib import Path

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


BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
TAROT = BASE_DIR / 'tarot'
MEDIA = BASE_DIR / 'media'
EASTER_EGGS = MEDIA / 'easter_eggs'
SHOP_DELIVERY = MEDIA / 'shop_delivery'
STUDIO_AND_DIRECTIONS = MEDIA / 'studio_and_directions'

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

CHANNEL_ID = int(getenv('CHANNEL_ID'))

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
CSV_PATH = 'data_dump/Users.csv'

INSTAGRAM = getenv('INSTAGRAM')
VK = getenv('VK')
TG_DM = getenv('TG_DM')
TG_CHANNEL = getenv('TG_CHANNEL')
WA = getenv('WA')
YA_DISK = getenv('YA_DISK')
SUPPORT = getenv('SUPPORT')
ORG_NAME = getenv('ORG_NAME')

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

HELP_KEYWORDS = [
    'вернуться', 'главное меню', 'где найти', 'инфо', 'информация',
    'инструкция', 'инструкции', 'как начать', 'меню', 'начало',
    'начать', 'начальное меню', 'навигация', 'поддержка', 'помощь',
    'подсказка', 'справка', 'что делать', 'help', 'main', 'menu'
]

STUDIO_KEYWORDS = [
    'информация о студии', 'инфо студии', 'о нас', 'о студии', 'работа студии',
    'студийная информация', 'студийное обучение', 'студия', 'творчество',
    'about', 'studio'
]

SHOP_KEYWORDS = [
    'ассортимент', 'доставка', 'заказать', 'каталог', 'купить', 'магазин',
    'магазин студии', 'новинки', 'оформить заказ', 'покупка', 'продажа',
    'продукция', 'продукты', 'студийные товары', 'студийный магазин',
    'товары', 'товары студии', 'заказы', 'shop', 'store'
]

MK_KEYWORDS = [
    'выездные мастер классы', 'записаться', 'класс', 'курс', 'курсы студии',
    'мастер классы', 'мастер-класс', 'мастер-классы студии', 'мк', 'навыки',
    'обучающие курсы', 'обучающий курс', 'обучение', 'обучение от студии',
    'студийные уроки', 'тренинг', 'учеба', 'учебная программа',
    'учебные занятия', 'учебные мастер-классы', 'учебные программы',
    'offsite', 'workshop'
]

SOC_PROFS_KEYWORDS = [
    'вк', 'вконтакте', 'галерея', 'изображения', 'инстаграм', 'контакты',
    'наши работы', 'наши проекты', 'наши соцсети', 'посмотреть работы',
    'портфолио', 'портфолио студии', 'профили', 'проекты', 'примеры',
    'примеры работ', 'публикации', 'связь', 'сообщества', 'соцсети',
    'смотреть проекты', 'студийное портфолио', 'студийные профили', 'страницы',
    'ссылки на соцсети', 'facebook', 'instagram', 'vk'
]

ADDITIONAL_INFO = (
    '<u>Уточняйте актуальное расписание, '
    'перечень изделий и наличие '
    'мест у мастера!</u>'
)
ADDITIONAL_INFO_OFFSITE = (
    '<u>Минимальное количество человек, перечень '
    'изделий и стоимость выезда на локацию проведения '
    'уточняйте у мастера!</u>'
)
