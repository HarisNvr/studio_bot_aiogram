from asyncio import sleep
from functools import wraps

from aiogram.exceptions import AiogramError
from aiogram.types import Message
from sqlalchemy import update, select

from core.database.background_tasks import (
    record_message_id_to_db, update_user, write_user
)
from core.database.engine import get_async_session
from core.database.models import User
from core.keyboards.main_kbs import unsubscribed_keyboard
from core.middleware.settings import (
    ADMIN_IDS, BOT, CHANNEL_ID, DEL_TIME
)
from core.utils.chepuha import chepuha


def check_bd_chat_id(function):
    """
    A decorator to check if a user's chat ID exists in the database.
    If not found, it suggests the user to press
    /start to initialize their chat session.

    :param function: The function to be decorated.
    :return: The decorated function.
    """

    @wraps(function)
    async def wrapper(message: Message, *args, **kwargs):
        chat_id = message.chat.id
        user_first_name = message.chat.first_name
        username = message.chat.username

        stmt = select(User).where(User.chat_id == chat_id)

        async for session in get_async_session():
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                if (user.username != username or
                        user.user_first_name != user_first_name):
                    await update_user(message)
            else:
                await write_user(message)

        return await function(message, *args, **kwargs)

    return wrapper


def check_is_admin(function):
    """
    A decorator that checks whether the user is an admin.

    :param function: The function to be decorated.
    :return: The decorated function.
    """

    @wraps(function)
    async def wrapper(message: Message, *args, **kwargs):
        await record_message_id_to_db(message)

        if message.chat.id in ADMIN_IDS:
            return await function(message, *args, **kwargs)
        else:
            await chepuha(message)

    return wrapper


def sub_check(function):
    """
    A decorator that checks if a user is subscribed to a telegram channel
    and sends a message if they are not.

    :param function: The function to be decorated.
    :return: The decorated function.
    """

    @wraps(function)
    async def wrapper(message: Message, *args, **kwargs):
        try:
            result = await BOT.get_chat_member(CHANNEL_ID, message.chat.id)

            if result.status.value in ['member', 'administrator', 'creator']:
                is_subscribed = True
            else:
                is_subscribed = False
        except AiogramError:
            is_subscribed = False

        stmt = update(User).where(User.chat_id == message.chat.id).values(
            is_subscribed=is_subscribed
        )

        async for session in get_async_session():
            await session.execute(stmt)
            await session.commit()

        if not is_subscribed and message.text == '/start':
            await sleep(DEL_TIME)
            sent_message = await BOT.send_message(
                chat_id=message.chat.id,
                text='<b>Я заметил, что вы не подписаны на наш ТГ канал, '
                'это никак не повлияет на мою работу, но мы были бы '
                'рады видеть вас в нашем крафт-сообществе</b> \U00002665',
                reply_markup=unsubscribed_keyboard
            )

            await record_message_id_to_db(sent_message)
            await sleep(DEL_TIME)

        return await function(message, *args, **kwargs)

    return wrapper
