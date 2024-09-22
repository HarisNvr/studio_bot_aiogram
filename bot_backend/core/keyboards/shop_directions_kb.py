from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

shop_directions_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='\U000026A1 Связаться с нами \U000026A1',
            url='https://t.me/elenitsa17'
        )
    ],
    [
        InlineKeyboardButton(
            text='Назад',
            callback_data='shop'
        )
    ]
])
