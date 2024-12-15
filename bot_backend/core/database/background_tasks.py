from datetime import datetime, timedelta

from aiogram.types import Message
from sqlalchemy import delete, select, update, insert, func

from core.components.settings import TZ
from core.database.db_connection import async_session_maker
from core.database.models import UserMessage, User
from core.utils.tg_channel import sub_check


async def morning_routine():
    """
    Delete old message IDs from the DB. Telegram's policy doesn't allow bots
    to delete messages that are older than 48 hours.

    :return: None
    """

    threshold = datetime.now(TZ) - timedelta(hours=48)
    stmt = delete(UserMessage).where(
        UserMessage.message_date < threshold
    )

    async with async_session_maker() as session:
        await session.execute(stmt)
        await session.commit()


async def get_user_id(message: Message) -> int | None:
    """
    Retrieves the user's primary key from the database using the chat id.

    :param message: The message sent by the user.
    :return: User's primary key - ID or None
    """

    stmt = select(User).where(User.chat_id == message.chat.id)

    async with async_session_maker() as session:
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            return user.id


async def record_message_id_to_db(*messages: Message):
    """
    Record message id's to DB, for 'clean' func.

    :param messages: The message sent by the user.
    :return: None
    """

    stmt_query = [
        insert(UserMessage).values(
            user_id=await get_user_id(message),
            message_id=message.message_id
        ) for message in messages
    ]

    async with async_session_maker() as session:
        for stmt in stmt_query:
            await session.execute(stmt)
        await session.commit()


async def write_user(message: Message):
    """
    Record user's data to DB.

    :param message: The message sent by the user.
    :return: None
    """

    is_subscribed = await sub_check(message.chat_id)

    stmt = insert(User).values(
        chat_id=message.chat.id,
        username=message.from_user.username,
        user_first_name=message.from_user.first_name,
        is_subscribed=is_subscribed
    )

    async with async_session_maker() as session:
        await session.execute(stmt)
        await session.commit()


async def update_user(message: Message):
    """
    Update user's data in DB.

    :param message: The message sent by the user.
    :return: None
    """

    is_subscribed = await sub_check(message.chat_id)

    stmt = update(User).where(User.chat_id == message.chat.id).values(
        username=message.from_user.username,
        user_first_name=message.from_user.first_name,
        is_subscribed=is_subscribed
    )

    async with async_session_maker() as session:
        await session.execute(stmt)
        await session.commit()


async def get_users_count() -> int:
    """
    Counts the number of users in the database.

    :return: User's count
    """

    stmt = select(func.count(User.id))

    async with async_session_maker() as session:
        result = await session.execute(stmt)
        count = result.scalar()

        return count
