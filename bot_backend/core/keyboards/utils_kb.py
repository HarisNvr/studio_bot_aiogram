from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

utils_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    ]
])
