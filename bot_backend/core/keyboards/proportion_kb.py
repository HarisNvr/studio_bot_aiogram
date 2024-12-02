from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

another_proportion_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Другая пропорция',
            callback_data='another_proportion'
        )
    ]
])

cancel_proportion_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_proportion'
        )
    ]
])
