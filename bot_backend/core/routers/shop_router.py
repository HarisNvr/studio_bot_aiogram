from aiogram import F, Router
from aiogram.types import CallbackQuery

from core.handlers.shop_handler import catalog, shipment, payment, ordering

shop_router = Router()

CALLBACKS = {'catalog', 'shipment', 'payment', 'ordering'}


@shop_router.callback_query(F.data.in_(CALLBACKS))
async def callback_router(callback: CallbackQuery):
    """
    Processes the incoming message callback data to determine if it matches
    any predefined cases and, if so, directs to the appropriate function.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    data = callback.data
    message = callback.message
    await callback.answer()

    if data == 'catalog':
        await catalog(message)
    elif data == 'shipment':
        await shipment(message)
    elif data == 'payment':
        await payment(message)
    elif data == 'ordering':
        await ordering(message)
