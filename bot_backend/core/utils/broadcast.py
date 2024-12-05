from asyncio import sleep
from datetime import datetime

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select

from core.database.background_tasks import record_message_id_to_db
from core.database.db_connection import async_session_maker
from core.database.models import User
from core.keyboards.utils_kbs import (
    init_broadcast_keyboard,
    confirm_broadcast_keyboard, get_broadcast_admin_keyboard
)
from core.middleware.fsm import BroadcastStates
from core.middleware.settings import DEL_TIME, BOT, TZ, ADMIN_IDS
from core.utils.format import get_word_form

broadcast_admin_id = None
"""
Stores the ID of the admin who is currently conducting a broadcast.
Initialized to None until an admin starts a broadcast.
"""

broadcast_func_messages_ids = []
"""
A list that stores the message IDs of messages sent during the broadcast 
process. This is used to keep track of messages for deletion after the 
broadcast is confirmed or canceled.
"""

broadcast_router = Router()


@broadcast_router.message(Command('broadcast'))
async def cmd_broadcast(message: Message, state: FSMContext):
    """
    Triggers by 'cmd_broadcast' function in admin router. Receive message from
    admin for broadcasting, lock the broadcast_admin_id variable to prevent
    multi-input errors and set BroadcastStates fsm state.

    :param message: The message sent by the admin.
    :param state: FSM context containing the state data.
    :return: None
    """

    global broadcast_admin_id

    if broadcast_admin_id is None:
        broadcast_admin_id = message.from_user.id

        await message.delete()
        await sleep(DEL_TIME)

        sent_message = await message.answer(
            text='Отправьте сообщение для рассылки',
            reply_markup=init_broadcast_keyboard
        )

        broadcast_func_messages_ids.append(sent_message.message_id)

        await state.set_state(BroadcastStates.broadcast_message)
    else:
        sent_message = await message.answer(
            'Сейчас идёт рассылка другого администратора'
        )

        await record_message_id_to_db(sent_message)


@broadcast_router.message(BroadcastStates.broadcast_message)
async def confirm_broadcast(message: Message, state: FSMContext):
    """
    Handles the 'broadcast_message' FSM state. Checks if the message's content
    type is suitable for broadcasting. If it is (text or photo), asks the admin
    to confirm the broadcast. If not, sends an error message to the admin.

    :param message: The message sent by the admin, containing content for
                    broadcasting.
    :param state: FSM context containing the state data.
    :return: None
    """

    broadcast_func_messages_ids.append(message.message_id)
    chat_id = message.chat.id
    content_type = message.content_type

    await state.update_data(broadcast_message=message)

    if content_type in ['text', 'photo']:
        sent_message = await message.answer(
            text='Разослать сообщение?',
            reply_markup=confirm_broadcast_keyboard
        )

        broadcast_func_messages_ids.append(sent_message.message_id)
    else:
        sent_message = await message.answer(
            text=f'<b>Неизвестный тип сообщения: {content_type}, '
                 'поддерживаются только тексты или '
                 'фотографии с описаниями</b>'
        )

        await sleep(DEL_TIME)

        while broadcast_func_messages_ids:
            func_message_id = broadcast_func_messages_ids.pop(0)
            await BOT.delete_message(chat_id, func_message_id)
            await sleep(0.2)

        global broadcast_admin_id

        await state.clear()
        broadcast_admin_id = None

        await sleep(10)
        await BOT.delete_message(chat_id, sent_message.message_id)


@broadcast_router.callback_query(F.data == 'send_broadcast')
async def send_broadcast(callback: CallbackQuery, state: FSMContext):
    """
    Handles the 'send_broadcast' callback query for sending a broadcast
    message. This function deletes any previous transitional messages, sends
    the broadcast to all users except admins, and notifies the admins about
    the status of the broadcast. Clears the 'broadcast_admin_id' variable and
    'broadcast_message' FSM state.

    :param callback: The callback query object containing information about
                     the message and chat.
    :param state: FSM context containing the state data.
    :return: None
    """

    global broadcast_admin_id
    global broadcast_func_messages_ids
    chat_id = callback.message.chat.id

    await callback.answer()

    while broadcast_func_messages_ids:
        func_message_id = broadcast_func_messages_ids.pop(0)
        await BOT.delete_message(chat_id, func_message_id)
        await sleep(0.2)

    await sleep(DEL_TIME)
    sent_message = await callback.message.answer(
        text='<b>РАССЫЛКА В ПРОЦЕССЕ</b>'
    )

    start_time = datetime.now(TZ).strftime('%d-%m-%Y %H:%M').split('.')[0]

    data = await state.get_data()
    broadcast_message = data['broadcast_message']
    broadcast_type = broadcast_message.content_type

    if broadcast_type == 'photo':
        broadcast_function = BOT.send_photo
        content_args = {'caption': broadcast_message.caption}
        content_value = broadcast_message.photo[-1].file_id
    else:
        broadcast_function = BOT.send_message
        content_args = {}
        content_value = broadcast_message.text

    stmt = select(User.chat_id)
    send_count = 0
    blocked_count = 0

    async with async_session_maker() as session:
        result = await session.execute(stmt)
        audience = result.scalars().all()

        for audience_chat_id in audience:
            if audience_chat_id not in ADMIN_IDS:
                try:
                    await broadcast_function(
                        audience_chat_id,
                        content_value,
                        **content_args
                    )
                    send_count += 1
                    await sleep(0.1)
                except AiogramError:
                    blocked_count += 1
                    pass

    await BOT.delete_message(chat_id, sent_message.message_id)
    await sleep(DEL_TIME)

    send_count_form = get_word_form(send_count, 'send')
    blocked_count_form = get_word_form(blocked_count, 'block')

    broadcast_success = (
        f'\U0001F6AB <b>{blocked_count}</b> {blocked_count_form} бота'
        f'\n\n\U0001F4E5 <b>{send_count}</b> {send_count_form} рассылку'
        f'\n\n\U0001F4C7 <b>Дата:</b> {start_time.split()[0]}'
        f'\n\n\U0000231A <b>Время:</b> {start_time.split()[1]}'
    )

    admin_link_keyboard = get_broadcast_admin_keyboard(broadcast_admin_id)

    for admin_id in ADMIN_IDS:
        markup = None

        if admin_id != broadcast_admin_id:
            markup = admin_link_keyboard

        await BOT.send_message(
            chat_id=admin_id,
            text=f'{broadcast_success}'
            '\n\n\U00002B07 <b>Содержание</b> \U00002B07',
            reply_markup=markup
        )

        await sleep(DEL_TIME)

        await broadcast_function(
            admin_id,
            content_value,
            **content_args
        )

    await state.clear()
    broadcast_admin_id = None


@broadcast_router.callback_query(F.data == 'cancel_broadcast')
async def cancel_broadcast(callback: CallbackQuery, state: FSMContext):
    """
    Handles the 'cancel_broadcast' callback query for canceling a broadcast
    message. This function deletes any previously sent broadcast-related
    messages, clears the 'broadcast_message' FSM state, clears
    'broadcast_admin_id' variable, and notifies the admin that the broadcast
    has been canceled.

    :param callback: The callback query object containing information about
                     the message and chat.
    :param state: FSM context containing the state data.
    :return: None
    """

    global broadcast_admin_id
    global broadcast_func_messages_ids
    chat_id = callback.message.chat.id

    await callback.answer()

    while broadcast_func_messages_ids:
        func_message_id = broadcast_func_messages_ids.pop(0)
        await BOT.delete_message(chat_id, func_message_id)
        await sleep(0.2)

    await state.clear()
    broadcast_admin_id = None

    await sleep(DEL_TIME)
    sent_message = await callback.message.answer(
        text='Рассылка отменена'
    )

    await sleep(5)
    await BOT.delete_message(chat_id, sent_message.message_id)
