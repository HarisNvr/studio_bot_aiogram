from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

offsite_keyboard = InlineKeyboardMarkup(inline_keyboard=[
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
            callback_data='studio'
        )
    ]
])
