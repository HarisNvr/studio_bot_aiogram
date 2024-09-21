from asyncio import sleep
from pathlib import Path

from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from core.database.background_tasks import record_message_id_to_db
from core.keyboards.studio_direction_keyboard import studio_direction_keyboard
from core.middleware.settings import BOT, DEL_TIME

ADDITIONAL_INFO = (
    '<u>Уточняйте актуальное расписание, '
    'перечень изделий и наличие '
    'мест у мастера!</u>'
)
ADDITIONAL_INFO_OFFSITE = (
    '<u>Минимальное количество человек, перечень '
    'изделий и стоимость выезда на локацию проведения '
    'уточняйте у мастера!</u>'
)

directions_router = Router()


@directions_router.callback_query(F.data == 'epoxy')
async def callback_epoxy(callback: CallbackQuery):
    """
    Handles the 'epoxy' callback query. Responds to the user and
    provides information about direction.

    :param callback:
    :return: None
    """

    await callback.answer()
    message = callback.message

    await BOT.delete_message(message.chat.id, message.message_id)
    await sleep(DEL_TIME)

    epoxy_photo_path = Path(
        __file__
    ).parent.parent.parent / '..' / 'studio_and_directions' / 'epoxy_img.png'
    epoxy_photo = FSInputFile(epoxy_photo_path)

    sent_message = await BOT.send_photo(
        chat_id=message.chat.id,
        photo=epoxy_photo,
        reply_markup=studio_direction_keyboard,
        caption='<b>Эпоксидная смола</b> - это '
                'универсальный '
                'материал, который позволяет '
                'создавать разнообразные изделия и '
                'декоративные элементы.'
                '\n'
                '\n На нашем занятии вы '
                'научитесь основам '
                'заливки. Мы покажем вам '
                'различные техники, '
                'а также расскажем о тонкостях '
                'при работе '
                'со смолой. Вы сможете создать свои '
                'уникальные и неповторимые '
                'изделия из смолы.'
                '\n'
                '\n Смола застывает в течении 24 часов. '
                'Своё изделие вы сможете забрать уже на '
                'следующий день. После отвердевания, '
                'смола становится безвредной и может '
                'контактировать с холодными продуктами.'
                '\n'
                '\n Мы обеспечим вам '
                'необходимую защитную '
                'экипировку: перчатки, респираторы и '
                'фартуки. Занятия проводятся в хорошо '
                'проветриваемом помещении.'
                '\n'
                '\n<u>Уточняйте актуальное расписание, '
                'перечень изделий и наличие '
                'мест у мастера!</u>',
    )

    await record_message_id_to_db(sent_message)


@directions_router.callback_query(F.data == ('gips' or 'gips_offsite'))
async def callback_gips(callback: CallbackQuery):
    """
    Handles the 'gips' or 'gips_offsite' callback query.
    Responds to the user and provides information about direction.

    :param callback:
    :return: None
    """

    await callback.answer()
    message = callback.message

    await BOT.delete_message(message.chat.id, message.message_id)
    await sleep(DEL_TIME)
