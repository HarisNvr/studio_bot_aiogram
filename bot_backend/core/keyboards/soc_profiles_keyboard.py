from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from core.middleware.settings import (
    INSTAGRAM, VK, TG_DM, WA, TG_CHANNEL, YA_DISK, SUPPORT
)

soc_profiles_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Instagram',
            url=INSTAGRAM
        ),
        InlineKeyboardButton(
            text='Группа VK',
            url=VK
        )
    ],
    [
        InlineKeyboardButton(
            text='Telegram',
            url=TG_DM
        ),
        InlineKeyboardButton(
            text='WhatsApp',
            url=WA
        )
    ],
    [
        InlineKeyboardButton(
            text='Наш канал в Telegram',
            url=TG_CHANNEL
        )
    ],
    [
        InlineKeyboardButton(
            text='Примеры работ на Я.Диск',
            url=YA_DISK
        )
    ],
    [
        InlineKeyboardButton(
            text='Тех. поддержка БОТА',
            url=SUPPORT
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    ]
])
