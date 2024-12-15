from asyncio import sleep
from functools import wraps

from aiogram.types import Message

from core.components.settings import ADMIN_IDS, BOT, DEL_TIME
from core.database.background_tasks import record_message_id_to_db
from core.keyboards.main_kbs import unsubscribed_keyboard
from core.utils.chepuha import chepuha
from core.utils.tg_channel import sub_check


def check_is_admin(function):
    """
    A decorator that checks whether the user is an admin.

    :param function: The function to be decorated.
    :return: The decorated function.
    """

    @wraps(function)
    async def wrapper(message: Message, *args, **kwargs):
        await record_message_id_to_db(message)

        if message.chat.id in ADMIN_IDS:
            return await function(message, *args, **kwargs)
        else:
            await chepuha(message)

    return wrapper


def sub_remind(function):
    """
    A decorator that checks if a user is subscribed to a telegram channel
    and sends a message if they are not.

    :param function: The function to be decorated.
    :return: The decorated function.
    """

    @wraps(function)
    async def wrapper(message: Message, *args, **kwargs):
        is_subscribed = await sub_check(message.chat.id)

        if not is_subscribed and message.text == '/start':
            await sleep(DEL_TIME)
            sent_message = await BOT.send_message(
                chat_id=message.chat.id,
                text='<b>Я заметил, что вы не подписаны на наш ТГ канал, '
                     'это никак не повлияет на мою работу, но мы были бы '
                     'рады видеть вас в нашем крафт-сообществе</b> \U00002665',
                reply_markup=unsubscribed_keyboard
            )

            await record_message_id_to_db(sent_message)
            await sleep(DEL_TIME)

        return await function(message, *args, **kwargs)

    return wrapper
