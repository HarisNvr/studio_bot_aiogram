from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db
from core.middleware.settings import EASTER_EGGS
from core.utils.chepuha import chepuha
from core.utils.path_builder import get_file


async def super_secret_func(message: Message):
    """
    TOP SECRET!!!

    :param message: Don't look here!
    :return: I'm serious! Go away!
    """

    some_dict = {
        'акуна': message.answer(text='Матата!'),
        'матата': message.answer(text='Акуна!'),
        'матата акуна': message.answer(text='\U0001F417 \U0001F439'),
        'акуна матата': message.answer_photo(
            photo=get_file(file_name='Akuna.jpg', directory=EASTER_EGGS)
        ),
        '\U0001F346': message.answer_photo(
            photo=get_file(file_name='bolt.png', directory=EASTER_EGGS)
        ),
        'hello world': message.answer_photo(
            photo=get_file(file_name='Hello-World.png', directory=EASTER_EGGS)
        )
    }

    try:
        sent_message = await some_dict[message.text.lower()]
        await record_message_id_to_db(message, sent_message)
    except KeyError:
        await chepuha(message)
