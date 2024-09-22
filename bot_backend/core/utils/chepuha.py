from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db


async def chepuha(message: Message):
    sent_message = await message.answer(
        text=f'Извините <u>{message.from_user.first_name}</u>, '
             'я вас не понимаю. '
             '\n'
             '\nПопробуйте написать '
             '/help для возврата в '
             'главное меню или воспользуйтесь '
             'кнопкой "Меню" '
             'около окна ввода сообщения'
    )

    await record_message_id_to_db(sent_message)
