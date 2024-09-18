from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

clean_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Да',
            callback_data='clean_chat'
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data='help'
        )
    ]
])
