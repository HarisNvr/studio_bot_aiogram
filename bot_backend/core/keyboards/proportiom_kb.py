from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

proportion_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Другая пропорция',
            callback_data='another_proportion'
        )
    ]
])
