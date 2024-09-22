from asyncio import sleep
from datetime import datetime

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.types import CallbackQuery
from sqlalchemy import select, delete, update

from core.database.background_tasks import get_user_id, record_message_id_to_db
from core.database.engine import get_async_session
from core.database.models import UserMessage, User
from core.handlers.user_router import (
    cmd_clean, cmd_help, cmd_soc_profiles, cmd_studio, cmd_mk
)
from core.keyboards.offsite_directions_keyboard import offsite_keyboard
from core.keyboards.studio_directions_keyboard import studio_keyboard
from core.middleware.settings import BOT, ADMIN_IDS, DEL_TIME
from core.utils.tarot import tarot_main

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


@callback_router.callback_query(F.data == 'studio')
async def callback_studio(callback: CallbackQuery):
    """
    Handles the 'studio' callback query. Responds to the user and
    triggers the studio command.

    :param callback:
    :return: None
    """

    await callback.answer()
    await cmd_studio(callback.message)


@callback_router.callback_query(F.data.startswith('directions_'))
async def callback_directions(callback: CallbackQuery):
    """
    Handles the 'directions_studio' or 'directions_offsite' callback query.
    Responds to the user and provides information about studio directions.

    :param callback:
    :return: None
    """

    await callback.answer()
    message = callback.message

    await BOT.delete_message(message.chat.id, message.message_id)
    await sleep(DEL_TIME)

    if callback.data == 'directions_studio':
        keyboard = studio_keyboard
    else:
        keyboard = offsite_keyboard

    sent_message = await message.answer(
        text='<b>Выберите <u>направление,</u> о котором хотите '
             'узнать подробнее:</b>',
        reply_markup=keyboard
    )

    await record_message_id_to_db(sent_message)


@callback_router.callback_query(F.data == 'mk')
async def callback_directions_offsite(callback: CallbackQuery):
    """
    Handles the 'directions_offsite' callback query. Responds to the user and
    provides information about offsite directions.

    :param callback:
    :return: None
    """

    await callback.answer()
    await cmd_mk(callback.message)


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


@callback_router.callback_query(F.data == 'tarot')
async def callback_tarot(callback: CallbackQuery):
    """
    Handles the 'tarot' callback query. Responds to the user and
    triggers the tarot layout func.

    :param callback:
    :return: None
    """

    await callback.answer()

    message = callback.message
    chat_id = message.chat.id
    user_first_name = message.chat.first_name

    stmt = select(User).where(User.chat_id == chat_id)

    async for session in get_async_session():
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        last_tarot_date = user.last_tarot_date
        if last_tarot_date:
            last_tarot_date = last_tarot_date.date()

        today = datetime.now()

        if chat_id in ADMIN_IDS:
            await BOT.delete_message(chat_id, message.message_id)
            await sleep(DEL_TIME)

            await tarot_main(message)
            await cmd_help(message, True)
        else:
            if last_tarot_date == today.date():
                sent_message = await message.answer(
                    text='<u>{user_first_name}</u>, '
                         'вы уже сегодня получили расклад, попробуйте завтра!'
                )

                await record_message_id_to_db(sent_message)
            else:
                stmt = update(User).where(
                    User.chat_id == chat_id
                ).values(
                    last_tarot_date=today
                )
                await session.execute(stmt)
                await session.commit()

                await BOT.delete_message(chat_id, message.message_id)
                await sleep(DEL_TIME)

                await tarot_main(message)
                await cmd_help(message, True)


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
    Handles the 'clean_chat' callback query from cmd_clean function.
    Cleans the chat by deleting messages from the database and the chat itself.

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
            text='<b>Идёт очистка чата</b> \U0001F9F9'
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
