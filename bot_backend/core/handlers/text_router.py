from aiogram import Router, F
from aiogram.types import Message

from core.handlers.user_router import cmd_help
from core.middleware.settings import HELP_KEYWORDS
from core.utils.secret import super_secret_func

text_router = Router()


@text_router.message(F.text)
async def text_to_func_handler(message: Message):
    """
    Processes the incoming message text to determine if it matches
    any predefined keywords and, if so, directs the message to the
    appropriate function.

    :param message: The message sent by the user.
    :return: None
    """

    if message.text.lower() in HELP_KEYWORDS:
        await cmd_help(message)
    else:
        await super_secret_func(message)
