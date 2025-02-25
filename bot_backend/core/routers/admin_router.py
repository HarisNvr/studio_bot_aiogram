from aiogram import Router, F
from aiogram.types import CallbackQuery, Message

from core.handlers.admin_handler import admin_menu, send_user
from core.utils.broadcast import broadcast_router

admin_router = Router()

admin_router.include_router(broadcast_router)

CALLBACKS = {'admin'}
COMMANDS = {'/users'}


@admin_router.callback_query(F.data.in_(CALLBACKS))
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

    if data == 'admin':
        await admin_menu(message)


@admin_router.message(F.text.in_(COMMANDS))
async def text_router(message: Message):
    """
    Processes the incoming command and directs to the appropriate function.

    :param message: The message sent by the admin.
    :return: None
    """

    message_text = message.text.lower()

    if message_text == '/users':
        await send_user(message)
