from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from core.middleware.settings import ADMIN_IDS


def get_main_keyboard(message: Message):
    """
    Creates a keyboard that contains buttons for the
    /start command, depending on the requesting user

    :param message: The message sent by the user.
    :return: Inline Keyboard Builder object
    """

    start_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text='О студии \U0001F393',
                callback_data='studio'
            )
        ],
        [
            InlineKeyboardButton(
                text='Наш магазин  \U0001F6CD',
                callback_data='shop'
            )
        ],
        [
            InlineKeyboardButton(
                text='Выездные МК  \U0001F30D',
                callback_data='mk'
            )
        ],
        [
            InlineKeyboardButton(
                text='#МыВСети \U0001F4F1',
                callback_data='soc_profiles'
            )
        ],
        [
            InlineKeyboardButton(
                text='Карты ТАРО \U00002728',
                callback_data='tarot'
            )
        ],
        [
            InlineKeyboardButton(
                text='Очистить чат \U0001F9F9',
                callback_data='clean'
            )
        ]
    ])

    start_markup = InlineKeyboardBuilder()
    start_markup.attach(InlineKeyboardBuilder.from_markup(start_keyboard))
    start_markup.adjust(2, 2, 2)

    if message.chat.id in ADMIN_IDS:
        start_markup.button(
            text='\U0001F60E Кнопка администратора \U0001F60E',
            callback_data='admin'
        )
        start_markup.adjust(2, 2, 2, 1)

    return start_markup
