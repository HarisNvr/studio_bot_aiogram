from asyncio import sleep

from aiogram.types import Message

from core.components.settings import DEL_TIME
from core.database.background_tasks import record_message_id_to_db
from core.keyboards.main_kbs import return_to_main_menu_kb


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
        reply_markup=return_to_main_menu_kb
    )

    await record_message_id_to_db(sent_message)
