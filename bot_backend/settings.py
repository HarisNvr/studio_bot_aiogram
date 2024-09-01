from os import getenv

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

load_dotenv()


def get_admin_ids():
    admin_ids = []
    for ADMIN_ID in (getenv('ADMIN_IDS').split(',')):
        admin_ids.append(int(ADMIN_ID))

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

INSTAGRAM = getenv('INSTAGRAM')
VK = getenv('VK')
TG_DM = getenv('TG_DM')
TG_CHANNEL = getenv('TG_CHANNEL')
WA = getenv('WA')
YA_DISK = getenv('YA_DISK')
SUPPORT = getenv('SUPPORT')
ORG_NAME = getenv('ORG_NAME')
CHANNEL_ID = int(getenv('CHANNEL_ID'))
