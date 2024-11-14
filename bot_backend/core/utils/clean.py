from asyncio import sleep

from aiogram.exceptions import AiogramError
from aiogram.types import Message
from sqlalchemy import select, delete

from core.database.background_tasks import get_user_id
from core.database.engine import get_async_session
from core.database.models import UserMessage
from core.middleware.settings import BOT


async def clean_chat(message: Message):
    """
    Cleans the chat by deleting messages from the database and the chat itself.

    :param message: The message sent by the user.
    :return: None
    """

    user_db_id = await get_user_id(message)

    stmt = select(
        UserMessage.message_id
    ).where(
        UserMessage.user_id == user_db_id
    )

    async for session in get_async_session():
        result = await session.execute(stmt)
        message_ids = result.scalars().all()

        await message.delete()

        sent_message = await message.answer(
            text='<b>Идёт очистка чата</b> \U0001F9F9'
        )

        for msg_id in message_ids:
            try:
                await BOT.delete_message(message.chat.id, msg_id)
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
