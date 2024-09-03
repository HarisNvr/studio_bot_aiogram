from datetime import datetime, timedelta
from subprocess import run
from time import sleep

from sqlalchemy import select, func, delete

from bot_backend.core.database.engine import session_maker
from bot_backend.core.database.models import Message, User
from bot_backend.core.middleware.settings import COMMIT_MESSAGE, MIGRATE


async def morning_routine():
    """
    Delete old message IDs from the DB. Telegram's policy doesn't allow bots
    to delete messages that are older than 48 hours. Wake's up a little bit
    slow, to give the database time to fully load.
    :return: Nothing
    """

    sleep(2)

    if MIGRATE:
        run(
            f'alembic revision --autogenerate -m "{COMMIT_MESSAGE}"',
            shell=True
        )
        run('alembic upgrade head', shell=True)
    else:
        threshold = datetime.now() - timedelta(hours=48)
        stmt = delete(Message).where(
            Message.message_date < threshold
        )

        async with session_maker() as session:
            await session.execute(stmt)
            await session.commit()


async def get_user_db_id(chat_id: int):
    """
    Retrieves the user's primary key from the database using the chat id.
    :param chat_id:
    :return: User's primary key - ID
    """

    async with session_maker() as session:
        stmt = select(User).where(User.chat_id == chat_id)
        result = await session.execute(stmt)
        user = result.scalar()

    return user.id if user else None


async def get_users_count():
    """
    Counts the number of users in the database.
    :return: User's count
    """

    async with session_maker() as session:
        count = await session.scalar(select(func.count(User.id)))

    return count


async def record_message_id_to_db(chat_id: int, message_id: int):
    """
    Record message id's to DB, for 'clean' func.
    :return: Nothing
    """

    async with session_maker() as session:
        session.add(
            Message(
                chat_id=chat_id,
                message_id=message_id,
            )
        )
        await session.commit()
