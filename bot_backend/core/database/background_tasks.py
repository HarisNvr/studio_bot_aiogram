from datetime import datetime, timedelta

from aiogram.types import Message
from sqlalchemy import delete, select, update, insert, func

from core.database.engine import get_async_session
from core.database.models import UserMessage, User
from core.middleware.settings import TZ


async def morning_routine():
    """
    Delete old message IDs from the DB. Telegram's policy doesn't allow bots
    to delete messages that are older than 48 hours.

    :return: Nothing
    """

    threshold = datetime.now(TZ) - timedelta(hours=48)
    stmt = delete(UserMessage).where(
        UserMessage.message_date < threshold
    )

    async for session in get_async_session():
        await session.execute(stmt)
        await session.commit()


async def get_user_id(message: Message):
    """
    Retrieves the user's primary key from the database using the chat id.

    :param message:
    :return: User's primary key - ID
    """

    stmt = select(User).where(User.chat_id == message.chat.id)

    async for session in get_async_session():
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if user:
            return user.id


async def record_message_id_to_db(message: Message):
    """
    Record message id's to DB, for 'clean' func.

    :param message:
    :return: Nothing
    """

    user_id = await get_user_id(message)
    stmt = insert(UserMessage).values(
        user_id=user_id,
        message_id=message.message_id
    )

    async for session in get_async_session():
        await session.execute(stmt)
        await session.commit()


async def write_user(message: Message):
    """
    Record user's data to DB.

    :param message:
    :return: Nothing
    """

    stmt = insert(User).values(
        chat_id=message.chat.id,
        username=message.from_user.username,
        user_first_name=message.from_user.first_name
    )

    async for session in get_async_session():
        await session.execute(stmt)
        await session.commit()


async def update_user(message: Message):
    """
    Update user's data in DB.

    :param message:
    :return: Nothing
    """

    stmt = update(User).where(User.chat_id == message.chat.id).values(
        username=message.from_user.username,
        user_first_name=message.from_user.first_name
    )

    async for session in get_async_session():
        await session.execute(stmt)
        await session.commit()


async def get_users_count():
    """
    Counts the number of users in the database.

    :return: User's count
    """

    stmt = select(func.count(User.id))

    async for session in get_async_session():
        result = await session.execute(stmt)
        count = result.scalar()

        return count
