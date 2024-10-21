from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from core.middleware.settings import TG_CHANNEL

markup_unsubscribed = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text='Наш канал в Telegram',
                url=TG_CHANNEL
            )
        ]
    ]
)
