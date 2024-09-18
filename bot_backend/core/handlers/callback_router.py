from asyncio import sleep

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.types import CallbackQuery
from sqlalchemy import select, delete

from core.database.background_tasks import get_user_id
from core.database.engine import get_async_session
from core.database.models import UserMessage
from core.handlers.user_router import (
    cmd_clean, cmd_help, cmd_soc_profiles
)
from core.middleware.settings import BOT


callback_router = Router()


@callback_router.callback_query(F.data == 'help')
async def callback_help(callback: CallbackQuery):
    """
    Handles the 'help' callback query. Responds to the user and
    triggers the help command.

    :param callback:
    :return: None
    """

    await callback.answer()
    await cmd_help(callback.message)


@callback_router.callback_query(F.data == 'soc_profiles')
async def callback_soc_profiles(callback: CallbackQuery):
    """
    Handles the 'soc_profiles' callback query. Responds to the user and
    triggers the social profiles command.

    :param callback:
    :return: None
    """

    await callback.answer()
    await cmd_soc_profiles(callback.message)


@callback_router.callback_query(F.data == 'clean')
async def callback_clean(callback: CallbackQuery):
    """
    Handles the 'clean' callback query. Responds to the user and
    triggers the clean command.

    :param callback:
    :return: None
    """

    await callback.answer()
    await cmd_clean(callback.message)


@callback_router.callback_query(F.data == 'clean_chat')
async def callback_clean_chat(callback: CallbackQuery):
    """
    Handles the 'clean_chat' callback query. Cleans the chat by
    deleting messages from the database and the chat itself.

    :param callback:
    :return: None
    """

    await callback.answer()

    message = callback.message
    chat_id = message.chat.id
    user_db_id = await get_user_id(message)

    stmt = select(
        UserMessage.message_id
    ).where(
        UserMessage.user_id == user_db_id
    )

    async for session in get_async_session():
        result = await session.execute(stmt)
        message_ids = result.scalars().all()

        await BOT.delete_message(chat_id, message.message_id)

        sent_message = await message.answer(
            text=f'<b>Идёт очистка чата</b> \U0001F9F9'
        )

        for msg_id in message_ids:
            try:
                await BOT.delete_message(chat_id, msg_id)
                await sleep(0.01)
            except AiogramError:
                pass

            await session.execute(
                delete(
                    UserMessage
                ).where(
                    UserMessage.user_id == user_db_id,
                    UserMessage.message_id == msg_id)
            )
        await session.commit()

        await BOT.delete_message(sent_message.chat.id, sent_message.message_id)
