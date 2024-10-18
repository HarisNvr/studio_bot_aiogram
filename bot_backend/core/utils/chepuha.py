from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db


async def chepuha(message: Message):
    """
    The best function ever! At least by its name. Handles any text messages
    from the user, that doesn't match the previous routers.

    :param message: The message sent by the user.
    :return: None
    """

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
