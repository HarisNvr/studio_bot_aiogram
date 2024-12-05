from aiogram import F, Router
from aiogram.types import CallbackQuery

from core.handlers.directions_handler import (
    directions_list, epoxy, gips, sketching, tie_dye, custom_cloth, candles
)

directions_router = Router()

CALLBACKS = {
    'directions_studio', 'directions_offsite',
    'gips', 'gips_offsite',
    'candles', 'candles_offsite',
    'tie_dye', 'tie_dye_offsite',
    'sketching',
    'custom_cloth',
    'epoxy'
}


@directions_router.callback_query(F.data.in_(CALLBACKS))
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

    if data.startswith('directions'):
        await directions_list(message, data)
    elif data == 'epoxy':
        await epoxy(message)
    elif data.startswith('gips'):
        await gips(message, data)
    elif data == 'sketching':
        await sketching(message)
    elif data.startswith('tie_dye'):
        await tie_dye(message, data)
    elif data == 'custom_cloth':
        await custom_cloth(message)
    elif data.startswith('candles'):
        await candles(message, data)
