from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_broadcast_admin_keyboard(broadcast_admin_id: int | str | None):
    """
    Creates a keyboard that contains button for the final report of the
    /broadcast command, depending on the broadcasting admin.

    :param broadcast_admin_id: Telegram ID of the broadcasting admin.
    :return: InlineKeyboardMarkup object.
    """

    if broadcast_admin_id:
        admin_link_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f'Ответственный администратор',
                    url=f'tg://user?id={broadcast_admin_id}'
                )
            ]
        ])
    else:
        admin_link_keyboard = None

    return admin_link_keyboard


init_broadcast_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel_broadcast'
        )
    ]
])

confirm_broadcast_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Разослать',
            callback_data='send_broadcast'
        ),
        InlineKeyboardButton(
            text='Отменить',
            callback_data='cancel_broadcast'
        )
    ]
])

another_proportion_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Другая пропорция',
            callback_data='another_proportion'
        )
    ]
])

cancel_proportion_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Отмена',
            callback_data='cancel_proportion'
        )
    ]
])

clean_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Да',
            callback_data='clean_chat'
        ),
        InlineKeyboardButton(
            text='Нет',
            callback_data='help'
        )
    ]
])
