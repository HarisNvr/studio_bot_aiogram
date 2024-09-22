from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

mk_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Подробнее о направлениях',
            callback_data='directions_offsite'
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
    ],
])
