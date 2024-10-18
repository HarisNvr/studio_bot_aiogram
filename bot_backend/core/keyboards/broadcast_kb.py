from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
