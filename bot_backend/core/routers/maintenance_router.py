from aiogram import F, Router
from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db

maintenance_router = Router()


@maintenance_router.message(F)
async def maintenance_handler(message: Message):
    """
    Handles any message during MAINTENANCE_MODE.

    :param message: The message sent by the user.
    :return: None
    """

    sent_message = await message.answer(
        text=f'Извините {message.from_user.first_name}, '
             f'сейчас ведутся тех. работы. Попробуйте написать мне позднее.'
    )
    await record_message_id_to_db(message, sent_message)
