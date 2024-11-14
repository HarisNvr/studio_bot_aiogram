from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

shop_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Как заказать \U00002705',
            callback_data='ordering'
        ),
        InlineKeyboardButton(
            text='Каталог \U0001F50D',
            callback_data='catalog'
        )
    ],
    [
        InlineKeyboardButton(
            text='Оплата \U0001F4B3',
            callback_data='payment'
        ),
        InlineKeyboardButton(
            text='Доставка \U0001F4E6',
            callback_data='shipment'
        )
    ],
    [
        InlineKeyboardButton(
            text='\U000026A1 Связаться с нами \U000026A1',
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
