from asyncio import sleep

from aiogram.types import Message
from more_itertools import chunked
from sqlalchemy import select, delete

from core.database.background_tasks import get_user_id
from core.database.engine import get_async_session
from core.database.models import UserMessage
from core.middleware.settings import BOT, DEL_TIME


async def clean_chat(message: Message):
    """
    Cleans the chat by deleting messages from the database and the chat itself.

    :param message: The message sent by the user.
    :return: None
    """

    user_db_id = await get_user_id(message)

    await message.delete()
    await sleep(DEL_TIME)

    stmt = select(
        UserMessage.message_id
    ).where(
        UserMessage.user_id == user_db_id
    )

    async for session in get_async_session():
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
