from asyncio import sleep

from aiogram.types import Message

from core.database.background_tasks import record_message_id_to_db
from core.keyboards.offsite_kbs import (
    to_offsite_directions_kb, offsite_directions_keyboard
)
from core.keyboards.studio_kbs import (
    studio_directions_keyboard, to_studio_directions_kb
)
from core.middleware.settings import (
    DEL_TIME, ADDITIONAL_INFO_OFFSITE, ADDITIONAL_INFO, STUDIO_AND_DIRECTIONS
)
from core.utils.path_builder import get_file


async def directions_list(message: Message, data: str):
    """
    Displays a list of directions based on the data provided.

    :param message: The message sent by the user.
    :param data: Callback data associated with the message.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    if data == 'directions_studio':
        keyboard = studio_directions_keyboard
    else:
        keyboard = offsite_directions_keyboard

    sent_message = await message.answer(
        text='<b>Выберите <u>направление,</u> о котором хотите '
             'узнать подробнее:</b>',
        reply_markup=keyboard
    )

    await record_message_id_to_db(sent_message)


async def epoxy(message: Message):
    """
    Handles the 'epoxy' callback query. Responds to the user and
    provides information about direction.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    epoxy_photo = get_file(
        file_name='epoxy_img.png',
        directory=STUDIO_AND_DIRECTIONS
    )
    epoxy_keyboard = to_studio_directions_kb

    sent_message = await message.answer_photo(
        photo=epoxy_photo,
        reply_markup=epoxy_keyboard,
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


async def gips(message: Message, data: str):
    """
    Handles the 'gips' or 'gips_offsite' callback query.
    Responds to the user and provides information about direction.

    :param message: The message sent by the user.
    :param data: Callback data associated with the message.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    gips_photo = get_file(
        file_name='gips_img.png',
        directory=STUDIO_AND_DIRECTIONS
    )

    if data == 'gips_offsite':
        gips_keyboard = to_offsite_directions_kb
        additional_info = ADDITIONAL_INFO_OFFSITE
    else:
        gips_keyboard = to_studio_directions_kb
        additional_info = ADDITIONAL_INFO

    sent_message = await message.answer_photo(
        photo=gips_photo,
        reply_markup=gips_keyboard,
        caption='<b>Гипс</b> - это универсальный '
                'и простой в работе материал, '
                'из которого можно создавать различные предметы декора и '
                'подарки.'
                '\n\n На нашем занятии вы познакомитесь с основами '
                'литья из гипса и узнаете, как изготавливать гипсовые '
                'изделия своими руками. '
                'Мы научим вас правильно замешивать '
                'гипсовый раствор, расскажем '
                'о секретах получения крепкого, '
                'ровного изделия с минимальным количеством пузырей.'
                '\n\n Вы сможете создать свои неповторимые '
                'изделия и украсить дом. Так же гипсовые изделия – это '
                'отличный подарок, сделанный своими руками.'
                f'\n\n{additional_info}'
    )

    await record_message_id_to_db(sent_message)


async def sketching(message: Message):
    """
    Handles the 'sketching' callback query.
    Responds to the user and provides information about direction.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    sketching_photo = get_file(
        file_name='sketch_img.png',
        directory=STUDIO_AND_DIRECTIONS
    )
    sketching_keyboard = to_studio_directions_kb

    sent_message = await message.answer_photo(
        photo=sketching_photo,
        reply_markup=sketching_keyboard,
        caption='<b>Скетчинг</b> - это техника быстрого '
                'рисования набросков и эскизов, которая '
                'помогает визуализировать идеи, эмоции и '
                'впечатления. На нашем '
                'занятии вы узнаете, '
                'как рисовать скетчи от '
                'руки с помощью разных '
                'материалов: карандашей, '
                'маркеров, пастели. '
                '\n'
                '\n  Вы научитесь выбирать '
                'подходящие объекты '
                'для скетчинга, определять перспективу и '
                'светотень, создавать '
                'композицию и цветовую '
                'гамму. Мы покажем вам различные стили и '
                'техники скетчинга. '
                '\n'
                '\n  Вы сможете создать свои уникальные '
                'скетчи на любые темы: '
                'природа, архитектура, '
                'мода и многое другое.'
                '\n'
                '\n<u>Уточняйте актуальное расписание '
                'и наличие мест у мастера!</u>'
    )

    await record_message_id_to_db(sent_message)


async def tie_dye(message: Message, data: str):
    """
    Handles the 'tie_dye' or 'tie_dye_offsite' callback query.
    Responds to the user and provides information about direction.

    :param message: The message sent by the user.
    :param data: Callback data associated with the message.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    tie_dye_photo = get_file(
        file_name='tie_dye_img.png',
        directory=STUDIO_AND_DIRECTIONS
    )

    if data == 'tie_dye_offsite':
        tie_dye_keyboard = to_offsite_directions_kb
        additional_info = ADDITIONAL_INFO_OFFSITE
    else:
        tie_dye_keyboard = to_studio_directions_kb
        additional_info = ADDITIONAL_INFO

    sent_message = await message.answer_photo(
        photo=tie_dye_photo,
        reply_markup=tie_dye_keyboard,
        caption='<b>Тай-дай</b> - это техника '
                'окрашивания ткани при помощи '
                'скручивания, которая позволяет '
                'создавать яркие и '
                'оригинальные узоры. На нашем '
                'занятии вы узнаете, как делать '
                'тай-дай своими руками. Вы научитесь выбирать подходящие '
                'красители и способы завязывания '
                'ткани для получения разных '
                'эффектов.\n\n Мы покажем вам различные стили и техники '
                'тай-дай: от классического спирального до современного '
                'мраморного. Вы сможете создать '
                'свои уникальные вещи в стиле '
                'тай-дай: футболки, платья, джинсы, шопперы и '
                'другое.\n\n<b>А также при помощи тай-дай можно подарить '
                'вторую жизнь своей любимой '
                'вещи.</b>'
                f'\n\n{additional_info}'
    )

    await record_message_id_to_db(sent_message)


async def custom_cloth(message: Message):
    """
    Handles the 'custom_cloth' callback query.
    Responds to the user and provides information about direction.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    custom_cloth_photo = get_file(
        file_name='cloth_img.png',
        directory=STUDIO_AND_DIRECTIONS
    )
    custom_cloth_keyboard = to_studio_directions_kb

    sent_message = await message.answer_photo(
        photo=custom_cloth_photo,
        reply_markup=custom_cloth_keyboard,
        caption='<b>Роспись одежды</b> - это творческий '
                'способ преобразить свои '
                'вещи и сделать их '
                'уникальными. На нашем '
                'занятии вы узнаете, '
                'как рисовать на ткани акриловыми '
                'красками и какие материалы, инструменты '
                'для этого нужны. '
                '\n'
                '\n  Вы научитесь выбирать '
                'подходящие рисунки '
                'и узоры, переносить их '
                'на одежду, а также '
                'использовать разные техники: от простых '
                'надписей, до полноценных картин. '
                'Мы покажем '
                'вам различные стили росписи: '
                'от классических '
                'цветочных мотивов до '
                'современных абстрактных '
                'рисунков. Вы сможете '
                'разрисовать свою одежду '
                'в соответствии со своим вкусом и стилем. '
                '\n'
                '\n  Мы используем специальные краски, '
                'которые не смываются с ткани. Поэтому '
                'расписанная вещь будет радовать '
                'вас очень долго.'
                '\n'
                '\n<u>Уточняйте актуальное расписание, '
                'перечень изделий и наличие '
                'мест у мастера!</u>'
    )

    await record_message_id_to_db(sent_message)


async def candles(message: Message, data: str):
    """
    Handles the 'candles' or 'candles_offsite' callback query.
    Responds to the user and provides information about direction.

    :param message: The message sent by the user.
    :param data: Callback data associated with the message.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    candles_photo = get_file(
        file_name='candles_img.png',
        directory=STUDIO_AND_DIRECTIONS
    )

    if data == 'candles_offsite':
        candles_keyboard = to_offsite_directions_kb
        additional_info = ADDITIONAL_INFO_OFFSITE
    else:
        candles_keyboard = to_studio_directions_kb
        additional_info = ADDITIONAL_INFO

    sent_message = await message.answer_photo(
        photo=candles_photo,
        reply_markup=candles_keyboard,
        caption='<b>Ароматические свечи</b> - это не '
                'только красивый и уютный '
                'элемент декора, но и способ создать особую атмосферу в '
                'доме.'
                '\n\n На нашем занятии вы создадите свечу своими руками '
                'из натуральных ингредиентов: соевого воска, '
                'хлопкового или деревянного фитиля. '
                'Вы сможете выбрать ароматы по своему вкусу '
                '(более 20 различных ароматов). '
                'Мы расскажем вам о '
                'тонкостях процесса изготовления свечей, а также о том, '
                'как правильно использовать и хранить их.'
                '\n\n Вы получите не только полезные знания и навыки, '
                'но и удовольствие от творчества и релаксации.'
                f'\n\n{additional_info}'
    )

    await record_message_id_to_db(sent_message)
