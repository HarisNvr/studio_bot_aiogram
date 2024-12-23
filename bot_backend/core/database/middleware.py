from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from sqlalchemy import select

from core.database.background_tasks import update_user, write_user
from core.database.db_connection import async_session_maker
from core.database.models import User


class CheckUserDataBaseMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        chat_id = event.chat.id
        user_first_name = event.chat.first_name
        username = event.chat.username

        stmt = select(User).where(User.chat_id == chat_id)

        async with async_session_maker() as session:
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                condition_one = user.username == username
                condition_two = user.user_first_name == user_first_name

                if not condition_one or not condition_two:
                    await update_user(event)
            else:
                await write_user(event)

        return await handler(event, data)
