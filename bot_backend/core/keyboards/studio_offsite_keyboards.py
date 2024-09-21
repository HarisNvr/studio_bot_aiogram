from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_studio_offsite_keyboard(is_offsite: bool):
    if not is_offsite:
        direction_keyboard = InlineKeyboardMarkup(inline_keyboard=[
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
    else:
        direction_keyboard = InlineKeyboardMarkup(inline_keyboard=[
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

    return direction_keyboard
