from asyncio import sleep

from aiogram import Router, F
from aiogram.exceptions import AiogramError
from aiogram.types import CallbackQuery
from sqlalchemy import select, delete

from core.database.background_tasks import get_user_id, record_message_id_to_db
from core.database.engine import get_async_session
from core.database.models import UserMessage
from core.handlers.user_router import (
    cmd_clean, cmd_help, cmd_soc_profiles, cmd_studio, cmd_mk, cmd_shop
)
from core.keyboards.offsite_directions_kb import offsite_keyboard
from core.keyboards.studio_directions_kb import studio_keyboard
from core.middleware.settings import BOT, DEL_TIME
from core.utils.tarot import tarot_start

callback_router = Router()


@callback_router.callback_query(F.data == 'help')
async def callback_help(callback: CallbackQuery):
    """
    Handles the 'help' callback query. Responds to the user and
    triggers the help command.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    await cmd_help(callback.message)


@callback_router.callback_query(F.data == 'studio')
async def callback_studio(callback: CallbackQuery):
    """
    Handles the 'studio' callback query. Responds to the user and
    triggers the studio command.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    await cmd_studio(callback.message)


@callback_router.callback_query(F.data == 'shop')
async def callback_shop(callback: CallbackQuery):
    """
    Handles the 'shop' callback query. Responds to the user and
    triggers the shop command.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    await cmd_shop(callback.message)


@callback_router.callback_query(F.data.startswith('directions_'))
async def callback_directions(callback: CallbackQuery):
    """
    Handles the 'directions_studio' or 'directions_offsite' callback query.
    Responds to the user and provides information about studio directions.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    message = callback.message

    await message.delete()
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

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    await cmd_mk(callback.message)


@callback_router.callback_query(F.data == 'soc_profiles')
async def callback_soc_profiles(callback: CallbackQuery):
    """
    Handles the 'soc_profiles' callback query. Responds to the user and
    triggers the social profiles command.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    await cmd_soc_profiles(callback.message)


@callback_router.callback_query(F.data == 'tarot')
async def callback_tarot(callback: CallbackQuery):
    """
    Handles the 'tarot' callback query. Responds to the user and
    triggers the tarot layout funcs.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()

    message = callback.message
    await tarot_start(message)


@callback_router.callback_query(F.data == 'clean')
async def callback_clean(callback: CallbackQuery):
    """
    Handles the 'clean' callback query. Responds to the user and
    triggers the clean command.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    await cmd_clean(callback.message)


@callback_router.callback_query(F.data == 'clean_chat')
async def callback_clean_chat(callback: CallbackQuery):
    """
    Handles the 'clean_chat' callback query from cmd_clean function.
    Cleans the chat by deleting messages from the database and the chat itself.

    :param callback: The callback query object containing information about
                     the message and chat.
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

        await callback.message.delete()

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
                UserMessage.user_id == user_db_id
            )
        )
        await session.commit()

        await BOT.delete_message(sent_message.chat.id, sent_message.message_id)
