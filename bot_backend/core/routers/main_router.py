from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from core.database.background_tasks import record_message_id_to_db
from core.handlers.main_handler import (
    cmd_start, cmd_help, cmd_studio, cmd_shop, cmd_mk, cmd_soc_profiles
)
from core.middleware.settings import (
    HELP_KEYWORDS, STUDIO_KEYWORDS, SHOP_KEYWORDS, MK_KEYWORDS, SOC_KEYWORDS
)
from core.utils.chepuha import chepuha
from core.utils.secret import super_secret_func
from core.utils.tarot import tarot_start

main_router = Router()


@main_router.message(F.text)
async def text_router(message: Message):
    """
    Processes the incoming message text to determine if it matches
    any predefined commands or keywords and, if so, directs the message to the
    appropriate function.

    :param message: The message sent by the user.
    :return: None
    """

    message_text = message.text.lower()

    if message_text == '/start':
        await cmd_start(message)
    elif message_text == '/help' or message_text in HELP_KEYWORDS:
        await cmd_help(message)
    elif message_text == '/studio' or message_text in STUDIO_KEYWORDS:
        await cmd_studio(message)
    elif message_text == '/shop' or message_text in SHOP_KEYWORDS:
        await cmd_shop(message)
    elif message_text == '/mk' or message_text in MK_KEYWORDS:
        await cmd_mk(message)
    elif message_text == '/soc_profiles' or message_text in SOC_KEYWORDS:
        await cmd_soc_profiles(message)
    else:
        await super_secret_func(message)


@main_router.callback_query()
async def callback_router(callback: CallbackQuery):
    """
    Processes the incoming message callback data to determine if it matches
    any predefined cases and, if so, directs to the appropriate function.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    data = callback.data
    message = callback.message
    await callback.answer()

    if data == 'help':
        await cmd_help(message)
    elif data == 'studio':
        await cmd_studio(message)
    elif data == 'shop':
        await cmd_shop(message)
    elif data == 'mk':
        await cmd_mk(message)
    elif data == 'soc_profiles':
        await cmd_soc_profiles(message)
    elif data == 'tarot':
        await tarot_start(message)


@main_router.message(F)
async def misc_router(message: Message):
    """
    Handles any message that doesn't match the previous parameters.

    :param message: The message sent by the user.
    :return: None
    """

    await record_message_id_to_db(message)
    await chepuha(message)  # Best func name ever!
