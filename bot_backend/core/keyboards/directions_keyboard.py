from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

directions_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Эпоксидная смола',
            callback_data='epoxy'
        ),
        InlineKeyboardButton(
            text='Гипс',
            callback_data='gips'
        )
    ],
    [
        InlineKeyboardButton(
            text='Скетчинг',
            callback_data='sketching'
        ),
        InlineKeyboardButton(
            text='Тай-Дай',
            callback_data='tie_dye'
        )
    ],
    [
        InlineKeyboardButton(
            text='Роспись одежды',
            callback_data='custom_cloth'
        ),
        InlineKeyboardButton(
            text='Свечеварение',
            callback_data='candles'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='studio'
        )
    ]
])
