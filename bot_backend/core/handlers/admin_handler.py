from asyncio import sleep

from aiogram.types import Message

from core.components.settings import DEL_TIME, BOT
from core.components.wrappers import check_is_admin
from core.database.background_tasks import (
    get_users_count, record_message_id_to_db
)
from core.keyboards.main_kbs import return_to_main_menu_kb


async def admin_menu(message: Message):
    """
    Handles the 'admin' callback query. Responds to the admin-user and
    shows admin menu.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text='<b>Добро пожаловать в меню администратора!</b>'
             '\n'
             '\n/broadcast - Начать процедуру рассылки'
             '\n'
             '\n/users - Узнать сколько пользователей в БД',
        reply_markup=return_to_main_menu_kb
    )

    await record_message_id_to_db(sent_message)


@check_is_admin
async def send_user_count(message: Message):
    """
    Handles the 'users' command. Responds to the admin-user and sends the
    user count.

    :param message: The message sent by the user.
    :return: None
    """

    count = await get_users_count()

    await message.delete()
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text=f'Количество пользователей в БД: {count}'
    )

    await sleep(3.5)
    await BOT.delete_message(message.chat.id, sent_message.message_id)
