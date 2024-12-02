from asyncio import sleep

from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from core.database.background_tasks import (
    get_users_count, record_message_id_to_db
)
from core.keyboards.admin_kb import admin_keyboard
from core.middleware.settings import DEL_TIME, BOT
from core.middleware.wrappers import check_is_admin
from core.utils.broadcast import start_broadcast


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
        text='<b>Добро пожаловать в админское меню!</b>'
             '\n'
             '\n/broadcast - Начать процедуру рассылки'
             '\n'
             '\n/users - Узнать сколько пользователей в БД',
        reply_markup=admin_keyboard
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


@check_is_admin
async def cmd_broadcast(message: Message, state: FSMContext):
    """
    Handles the 'broadcast' command. Responds to the admin-user and starts a
    broadcast sequence.

    :param message: The message sent by the user.
    :param state: FSM context containing the state data.
    :return: None
    """

    await start_broadcast(message, state=state)
