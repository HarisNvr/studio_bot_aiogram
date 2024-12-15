from aiogram.exceptions import AiogramError

from core.components.settings import BOT, CHANNEL_ID


async def sub_check(chat_id: int) -> bool:
    """
    A function that checks if a user is subscribed to a
    telegram channel or not.

    :param chat_id: The chat_id of the user.
    :return: Boolean value indicating whether the user is subscribed
             to the channel or not:
             True if the user is a member, administrator, or creator
             of the channel.
             False if the user is not subscribed or if an error occurs.
    """

    try:
        result = await BOT.get_chat_member(CHANNEL_ID, chat_id)

        if result.status.value in ['member', 'administrator', 'creator']:
            is_subscribed = True
        else:
            is_subscribed = False
    except AiogramError:
        is_subscribed = False

    return is_subscribed
