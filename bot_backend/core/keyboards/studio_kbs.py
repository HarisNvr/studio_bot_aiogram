from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

studio_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Подробнее о направлениях',
            callback_data='directions_studio'
        )
    ],
    [
        InlineKeyboardButton(
            text='Наша студия в 2GIS',
            url='https://go.2gis.com/8od46'
        )
    ],
    [
        InlineKeyboardButton(
            text='\U000026A1 Записаться на МК \U000026A1',
            url='https://t.me/elenitsa17'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='help'
        )
    ]
])

studio_directions_keyboard = InlineKeyboardMarkup(inline_keyboard=[
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

to_studio_directions_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='\U000026A1 Записаться на МК \U000026A1',
            url='https://t.me/elenitsa17'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='directions_studio'
        )
    ]
])
