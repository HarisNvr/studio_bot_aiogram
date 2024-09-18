from asyncio import sleep

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db
from core.keyboards.clean_keyboard import clean_keyboard
from core.keyboards.soc_profiles_keyboard import soc_profiles_keyboard
from core.keyboards.start_keyboard import get_start_keyboard
from core.middleware.settings import BOT, DEL_TIME
from core.middleware.wrappers import check_bd_chat_id, sub_check
from core.utils.lang_greet import get_lang_greet_text

user_router = Router()


@user_router.message(Command('start'))
@check_bd_chat_id
@sub_check
async def cmd_start(message: Message):
    """
    Handles the '/start' command when a user initiates
    a conversation with the bot.

    :param message:
    :return:
    """

    await record_message_id_to_db(message)

    bot_info = await BOT.get_me()
    bot_name = bot_info.username
    start_keyboard = get_start_keyboard(message)

    sent_message = await message.answer(
        text=f'<b>Здравствуйте, '
             f'<u>{message.from_user.first_name}</u>! \U0001F642'
             f'\nМеня зовут {bot_name}.</b>'
             f'\nЧем я могу вам помочь?',
        reply_markup=start_keyboard.as_markup()
    )

    await record_message_id_to_db(sent_message)


@user_router.message(Command('help'))
@check_bd_chat_id
async def cmd_help(message: Message, keep_last_msg: bool = False):
    """
    Handles the '/help' command when a user calls the main menu.

    :param keep_last_msg: A Boolean value that determines whether the previous
        message will be deleted
    :param message:
    :return:
    """

    await record_message_id_to_db(message)

    if not keep_last_msg:
        await BOT.delete_message(message.chat.id, message.message_id)

    await sleep(DEL_TIME)

    start_keyboard = get_start_keyboard(message)

    sent_message = await message.answer(
        get_lang_greet_text(message.chat.first_name),
        reply_markup=start_keyboard.as_markup()
    )

    await record_message_id_to_db(sent_message)


@user_router.message(Command('soc_profiles'))
@check_bd_chat_id
async def cmd_soc_profiles(message: Message):
    """
    Handles the '/soc_profiles' command and sends a list of company contacts.

    :param message:
    :return:
    """

    await BOT.delete_message(message.chat.id, message.message_id)
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text=f'<b>Какая <u>соц.сеть</u>, вас интересует:</b>',
        reply_markup=soc_profiles_keyboard
    )

    await record_message_id_to_db(sent_message)


@user_router.message(Command('clean'))
@check_bd_chat_id
async def cmd_clean(message: Message):
    """
    Handles the '/clean' command and initiates the chat cleaning.

    :param message:
    :return:
    """

    await BOT.delete_message(message.chat.id, message.message_id)
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text='Вы хотите полностью очистить этот чат?'
             f'\n\n*Сообщения, отправленные более 48ч. назад и рассылка '
             f'удалены не будут',
        reply_markup=clean_keyboard
    )

    await record_message_id_to_db(sent_message)
