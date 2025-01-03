from asyncio import sleep

from aiogram.types import Message

from core.components.settings import DEL_TIME, SHOP_DELIVERY
from core.database.background_tasks import record_message_id_to_db
from core.keyboards.shop_kbs import shop_directions_keyboard
from core.utils.path_builder import get_file


async def catalog(message: Message):
    """
    Handles the 'catalog' callback query. Responds to the user and
    sends a PDF catalog to a user.

    :param message: The message sent by the user.
    :return: None
    """

    pdf_file = get_file(
        file_name='CSA_catalog.pdf',
        directory=SHOP_DELIVERY
    )

    sent_message = await message.answer_document(
        document=pdf_file,
        caption='Представляем наш каталог в формате PDF!'
                '\n\n<u>Не является публичной офертой! '
                '\nАктуальные цены уточняйте у сотрудников студии.</u>'
                '\n\n<b>Редакция от 13.07.2023</b>'
    )

    await record_message_id_to_db(sent_message)


async def shipment(message: Message):
    """
    Handles the 'shipment' callback query. Responds to the user and
    sends the shipment information.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    shipment_photo = get_file(
        file_name='shipment.jpg',
        directory=SHOP_DELIVERY
    )

    sent_message = await message.answer_photo(
        photo=shipment_photo,
        reply_markup=shop_directions_keyboard,
        caption='<b>После изготовления вашего заказа, '
                'на следующий рабочий день мы начинаем '
                'процесс доставки, который '
                'включает в себя следующее:</b>'
                '\n'
                '\n <u>ШАГ 1</u>: '
                'Бережно и надёжно упакуем ваш заказ '
                '\n'
                '\n <u>ШАГ 2</u>: '
                'Отвезем его в выбранную '
                'вами транспортную '
                'компанию (СДЕК, DPD, '
                'Boxberry, почта России)'
                '\n'
                '\n <u>ШАГ 3</u>: В течение '
                'нескольких дней '
                'вы сможете получить ваш заказ'
                '\n'
                '\n Если у вас остались '
                'какие-либо вопросы, '
                'касательно процесса доставки - вы всегда '
                'можете написать нам!'
    )

    await record_message_id_to_db(sent_message)


async def payment(message: Message):
    """
    Handles the 'pay' callback query. Responds to the user and
    sends the information about paying.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    payment_photo = get_file(
        file_name='payment.png',
        directory=SHOP_DELIVERY
    )

    sent_message = await message.answer_photo(
        photo=payment_photo,
        reply_markup=shop_directions_keyboard,
        caption='<u>После выбора товаров '
                'и их характеристик, '
                'а также согласования с '
                'мастером - вам будет '
                'предложено оплатить заказ.</u>'
                '\n'
                '\n<b>Обращаем ваше внимание, '
                'что наша студия '
                'работает только по 100% предоплате!</b>'
                '\n'
                '\n Мы принимаем банковские '
                'переводы на карту '
                'или по СБП, если вам необходим чек '
                'для отчётности - мы вам его предоставим. '
                'После получения оплаты мы начинаем '
                'изготовление вашего заказа в рамках '
                'согласованного заранее срока'
    )

    await record_message_id_to_db(sent_message)


async def ordering(message: Message):
    """
    Handles the 'order' callback query. Responds to the user and
    sends information about order process.

    :param message: The message sent by the user.
    :return: None
    """

    await message.delete()
    await sleep(DEL_TIME)

    ordering_photo = get_file(
        file_name='ordering.jpg',
        directory=SHOP_DELIVERY
    )

    sent_message = await message.answer_photo(
        photo=ordering_photo,
        reply_markup=shop_directions_keyboard,
        caption='<b>Заказать красивое '
                'изделие ручной работы '
                'очень просто! Вам потребуется:</b>'
                '\n'
                '\n1) Выбрать из каталога товар, '
                'который вам понравился.'
                '\n'
                '\n2) Запомнить порядковый '
                'номер этого товара.'
                '\n'
                '\n3) Написать нам номер/номера '
                'товаров, которые вы хотели бы заказать. '
                'Наш мастер подскажет, '
                'какие цвета/ароматы '
                'доступны для данного '
                'типа товара, а также '
                'ответит на интересующие вопросы.'
                '\n'
                '\n<u>Фотографии из каталога являются '
                'исключительно ознакомительными. '
                'Мы не гарантируем 100% повторения '
                'изделия с фото, т.к. каждое изделие '
                'изготавливается вручную "с нуля".</u>'
    )

    await record_message_id_to_db(sent_message)
