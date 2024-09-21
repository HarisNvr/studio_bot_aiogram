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
            text='Назад',
            callback_data='help'
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
    ]
])
