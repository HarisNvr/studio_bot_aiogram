from aiogram import Router, F
from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db
from core.utils.chepuha import chepuha

misc_router = Router()


@misc_router.message(F)
async def misc_handler(message: Message):
    await record_message_id_to_db(message)
    await chepuha(message)
