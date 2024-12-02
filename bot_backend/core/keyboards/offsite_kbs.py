from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

offsite_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Подробнее о направлениях',
            callback_data='directions_offsite'
        )
    ],
    [
        InlineKeyboardButton(
            text='\U000026A1 Забронировать МК \U000026A1',
            url='https://t.me/elenitsa17'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    ],
])

offsite_directions_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Гипс',
            callback_data='gips_offsite'
        )
    ],
    [
        InlineKeyboardButton(
            text='Тай-Дай',
            callback_data='tie_dye_offsite'
        )
    ],
    [
        InlineKeyboardButton(
            text='Свечеварение',
            callback_data='candles_offsite'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='mk'
        )
    ]
])

to_offsite_directions_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='\U000026A1 Забронировать МК \U000026A1',
            url='https://t.me/elenitsa17'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='directions_offsite'
        )
    ]
])
