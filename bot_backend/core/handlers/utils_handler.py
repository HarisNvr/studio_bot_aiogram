from asyncio import sleep

from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db
from core.keyboards.utils_kb import utils_keyboard
from core.middleware.settings import DEL_TIME


async def utils_menu(message: Message):
    """
    Handles the 'utils' callback query. Responds to the user and
    shows the utils menu.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text='<b>Добро пожаловать в меню полезных утилит!</b>'
             '\n'
             '\n/proportions - Калькулятор пропорций',
        reply_markup=utils_keyboard
    )

    await record_message_id_to_db(sent_message)
