from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from core.handlers.utils_handler import utils_menu
from core.utils.clean import clean_router
from core.utils.proportions import proportions_router

utils_router = Router()

utils_router.include_routers(
    clean_router,
    proportions_router
)

CALLBACKS = {'utils'}
COMMANDS = {'/utils'}


@utils_router.callback_query(F.data.in_(CALLBACKS))
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

    if data == 'utils':
        await utils_menu(message)


@utils_router.message(F.text.in_(COMMANDS))
async def text_router(message: Message):
    """
    Processes the incoming command and directs to the appropriate function.

    :param message: The message sent by the user.
    :return: None
    """

    message_text = message.text.lower()

    if message_text == '/utils':
        await utils_menu(message)
