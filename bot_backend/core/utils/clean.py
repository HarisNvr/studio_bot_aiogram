from asyncio import sleep

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from more_itertools import chunked
from sqlalchemy import select, delete

from core.database.background_tasks import get_user_id, record_message_id_to_db
from core.database.db_connection import async_session_maker
from core.database.models import UserMessage
from core.keyboards.utils_kbs import clean_keyboard
from core.middleware.settings import BOT, DEL_TIME
from core.middleware.wrappers import check_bd_chat_id

clean_router = Router()


@check_bd_chat_id
@clean_router.message(Command('clean'))
async def cmd_clean(message: Message):
    """
    Handles the '/clean' command and initiates the chat cleaning.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text='Вы хотите полностью очистить этот чат?'
             '\n\n*Сообщения, отправленные более 48ч. назад и рассылка '
             'удалены не будут',
        reply_markup=clean_keyboard
    )

    await record_message_id_to_db(sent_message)


@clean_router.callback_query(F.data == 'clean')
async def callback_clean(callback: CallbackQuery):
    """
    Handles the 'clean' callback query and initiates the chat cleaning.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    await cmd_clean(callback.message)


@clean_router.callback_query(F.data == 'clean_chat')
async def clean_chat(callback: CallbackQuery):
    """
    Cleans the chat by deleting messages from the database and the chat itself.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    message = callback.message
    user_db_id = await get_user_id(message)

    await message.delete()
    await sleep(DEL_TIME)

    stmt = select(
        UserMessage.message_id
    ).where(
        UserMessage.user_id == user_db_id
    )

    async with async_session_maker() as session:
        result = await session.execute(stmt)
        message_ids = result.scalars().all()

        await session.execute(
            delete(
                UserMessage
            ).where(
                UserMessage.user_id == user_db_id
            )
        )
        await session.commit()

        message_chunks = list(chunked(message_ids, 100))

        for msg_list in message_chunks:
            await BOT.delete_messages(
                chat_id=message.chat.id,
                message_ids=msg_list
            )

            await sleep(0.5)
