from pathlib import Path

from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from core.database.background_tasks import record_message_id_to_db
from core.utils.chepuha import chepuha

text_router = Router()


@text_router.message(F.text)
async def super_secret_func(message: Message):
    """
    TOP SECRET!!!

    :param message: Don't look here!
    :return: I'm serious! Go away!
    """

    await record_message_id_to_db(message)

    def get_photo(photo_name: str):
        """
        Prepare file for sending to user.

        :param photo_name: Photo's full name with extension.
        :return: An FSInputFile object containing the photo.
        """

        path = Path(
            __file__
        ).parent.parent.parent / '..' / 'easter_eggs' / photo_name
        return FSInputFile(path)

    some_dict = {
        'акуна': message.answer('Матата!'),
        'матата': message.answer('Акуна!'),
        'матата акуна': message.answer('\U0001F417 \U0001F439'),
        'акуна матата': message.answer_photo(get_photo('Akuna.jpg')),
        '\U0001F346': message.answer_photo(get_photo('bolt.png')),
        'hello world': message.answer_photo(get_photo('Hello-World.png'))
    }

    try:
        sent_message = await some_dict[message.text.lower()]
        await record_message_id_to_db(sent_message)
    except KeyError:
        await chepuha(message)
