from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_studio_offsite_keyboard(is_offsite: bool):
    """
    Creates a keyboard that contains buttons for the studio or offsite
    directions return, depending on the type of directions.

    :param is_offsite: Specifies if the buttons are for an offsite directions
                       or studio.
    :return: InlineKeyboardMarkup object.
    """

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
