from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

studio_direction_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='\U000026A1 Записаться на МК \U000026A1',
            url='https://t.me/elenitsa17'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='studio_directions'
        )
    ]
])
