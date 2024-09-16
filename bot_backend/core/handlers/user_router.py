from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db
from core.keyboards.start_keyboard import get_start_keyboard
from core.middleware.settings import BOT

user_router = Router()


@user_router.message(Command('start'))
async def cmd_start(message: Message):
    """

    :param message:
    :return:
    """

    await record_message_id_to_db(message)

    bot_info = await BOT.get_me()
    bot_name = bot_info.username
    start_keyboard = await get_start_keyboard(message)

    sent_message = await message.answer(
        text=f'<b>Здравствуйте, '
             f'<u>{message.from_user.first_name}</u>! \U0001F642'
             f'\nМеня зовут {bot_name}.</b>'
             f'\nЧем я могу вам помочь?',
        reply_markup=start_keyboard.as_markup()
    )

    await record_message_id_to_db(sent_message)
