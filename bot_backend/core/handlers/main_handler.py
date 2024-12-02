from asyncio import sleep

from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db
from core.keyboards.main_kbs import get_main_keyboard
from core.keyboards.offsite_kbs import offsite_keyboard
from core.keyboards.shop_kbs import shop_keyboard
from core.keyboards.soc_profiles_kb import soc_profiles_keyboard
from core.keyboards.studio_kbs import studio_keyboard
from core.keyboards.utils_kbs import clean_keyboard
from core.middleware.settings import (
    BOT, DEL_TIME, STUDIO_AND_DIRECTIONS, SHOP_DELIVERY
)
from core.middleware.wrappers import check_bd_chat_id, sub_check
from core.utils.lang_greet import get_lang_greet_text
from core.utils.path_builder import get_file


@check_bd_chat_id
@sub_check
async def cmd_start(message: Message):
    """
    Handles the '/start' command when a user initiates
    a conversation with the bot.

    :param message: The message sent by the user.
    :return: None
    """

    bot_info = await BOT.get_me()
    bot_name = bot_info.username
    start_keyboard = get_main_keyboard(message)

    sent_message = await message.answer(
        text='<b>Здравствуйте, '
             f'<u>{message.from_user.first_name}</u>! \U0001F642'
             f'\nМеня зовут {bot_name}.</b>'
             '\nЧем я могу вам помочь?',
        reply_markup=start_keyboard.as_markup()
    )

    await record_message_id_to_db(message, sent_message)


@check_bd_chat_id
async def cmd_help(message: Message, keep_last_msg: bool = False):
    """
    Handles the '/help' command when a user calls the main menu.

    :param keep_last_msg: A boolean value that determines whether the previous
                          message will be deleted.
    :param message: The message sent by the user.
    :return: None
    """

    if not keep_last_msg:
        await message.delete()

    await sleep(DEL_TIME)

    help_keyboard = get_main_keyboard(message)

    sent_message = await message.answer(
        get_lang_greet_text(message.chat.first_name),
        reply_markup=help_keyboard.as_markup()
    )

    if not keep_last_msg:
        await record_message_id_to_db(sent_message)
    else:
        await record_message_id_to_db(message, sent_message)


@check_bd_chat_id
async def cmd_studio(message: Message):
    """
    Handles the '/studio' command and provides information about the studio.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    studio_photo = get_file(
        file_name='studio_img.png',
        directory=STUDIO_AND_DIRECTIONS
    )

    sent_message = await message.answer_photo(
        photo=studio_photo,
        reply_markup=studio_keyboard,
        caption='<b>Наша мастерская</b> – это то место, '
                'где вы сможете раскрыть '
                'свой потенциал и '
                'реализовать идеи в разных направлениях: '
                'свечеварение, эпоскидная смола, '
                'рисование, '
                'роспись одежды и многое другое. '
                '\n'
                '\n\U0001F4CD<u>Наши адреса:'
                '\n</u><b>\U00002693 г. Новороссийск, '
                'с. Цемдолина, ул. Цемесская, д. 10'
                '\n\U00002600 г. Анапа, с. Витязево, '
                'ул. Курганная, д. 29</b>'
    )

    await record_message_id_to_db(sent_message)


@check_bd_chat_id
async def cmd_shop(message: Message):
    """
    Handles the '/shop' command and provides information about the studio shop.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    shop_photo = get_file(
        file_name='craft_shop.png',
        directory=SHOP_DELIVERY
    )

    sent_message = await message.answer_photo(
        photo=shop_photo,
        reply_markup=shop_keyboard,
        caption='<b>Добро пожаловать в наш '
                'крафтовый магазин \U00002728</b>'
                '\n'
                '\n Здесь вы найдете уникальные и '
                'качественные изделия ручной работы, '
                'созданные с любовью и нежностью. '
                'Мы предлагаем вам широкий ассортимент '
                'товаров: декор для дома, подарки, '
                'украшения, сухоцветы и многое другое.'
                '\n'
                '\n <b>Мы гарантируем вам:</b> '
                '<u>высокое качество, '
                'индивидуальный подход '
                'и быструю отправку.</u>'
    )

    await record_message_id_to_db(sent_message)


@check_bd_chat_id
async def cmd_mk(message: Message):
    """
    Handles the '/mk' command and provides information about offsite workshops.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    mk_photo = get_file(
        file_name='offsite_img.png',
        directory=STUDIO_AND_DIRECTIONS
    )

    sent_message = await message.answer_photo(
        photo=mk_photo,
        reply_markup=offsite_keyboard,
        caption='<b>Вы хотите удивить гостей '
                'творческим мастер–классом?</b> '
                '\n'
                '\n Наша студия готова приехать к вам c '
                'оборудованием и материалами '
                'по любой теме '
                'из нашего каталога: свечеварение, '
                'рисование, '
                'роспись одежды и другие. '
                'Мы обеспечим все '
                'необходимое для проведения МК в любом '
                'месте – в помещении или '
                'на свежем воздухе. '
                '\n'
                '\n <u>Все гости получат новые '
                'знания, навыки '
                'и подарки, сделанные своими руками!</u>'
    )

    await record_message_id_to_db(sent_message)


@check_bd_chat_id
async def cmd_soc_profiles(message: Message):
    """
    Handles the '/soc_profiles' command and sends a list of company contacts.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text='<b>Какая <u>соц.сеть</u>, вас интересует:</b>',
        reply_markup=soc_profiles_keyboard
    )

    await record_message_id_to_db(sent_message)


@check_bd_chat_id
async def cmd_clean(message: Message):
    """
    Handles the '/clean' command and initiates the chat cleaning.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text='Вы хотите полностью очистить этот чат?'
             '\n\n*Сообщения, отправленные более 48ч. назад и рассылка '
             'удалены не будут',
        reply_markup=clean_keyboard
    )

    await record_message_id_to_db(sent_message)
