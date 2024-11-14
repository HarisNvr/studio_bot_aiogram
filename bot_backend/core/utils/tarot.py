from asyncio import sleep
from datetime import datetime
from random import choice

from aiogram.types import Message, FSInputFile
from sqlalchemy import select, func, update

from core.database.background_tasks import record_message_id_to_db
from core.database.engine import get_async_session
from core.database.models import User
from core.handlers.main_handler import cmd_help
from core.middleware.settings import (
    BOT, ORG_NAME, TZ, TZ_STR, ADMIN_IDS, DEL_TIME, TAROT
)


async def tarot_start(message: Message):
    """
    Initiates a tarot card reading for the user. This function checks if
    the user has already received a tarot reading today. If not, it records
    the current date in the user's data, deletes the initial message, and
    calls the main tarot reading function followed by the help command.

    :param message: The message sent by the user.
    :return: None
    """

    chat_id = message.chat.id
    user_first_name = message.chat.first_name

    today = datetime.now(TZ).date()

    async for session in get_async_session():
        stmt = select(User).where(
            User.chat_id == chat_id,
            func.date(
                func.timezone(
                    TZ_STR,
                    User.last_tarot_date
                )
            ) == today
        )
        result = await session.execute(stmt)
        user = result.scalar_one_or_none()

        if chat_id in ADMIN_IDS:
            await message.delete()
            await sleep(DEL_TIME)

            await tarot_main(message)
            await cmd_help(message, keep_last_msg=True)
        else:
            if user:
                sent_message = await message.answer(
                    text=f'<u>{user_first_name}</u>, '
                         'вы уже сегодня получили расклад, попробуйте завтра!'
                )

                await record_message_id_to_db(sent_message)
            else:
                stmt = update(User).where(
                    User.chat_id == chat_id
                ).values(
                    last_tarot_date=datetime.now(TZ)
                )
                await session.execute(stmt)
                await session.commit()

                await message.delete()
                await sleep(DEL_TIME)

                await tarot_main(message)
                await cmd_help(message, keep_last_msg=True)


async def tarot_main(message: Message):
    """
    Handle the main logic for a tarot card reading. This function sends an
    introductory disclaimer message, selects 3 random tarot cards, and sends
    their images with descriptions to the user.

    :param message: The message sent by the user.
    :return: None
    """

    tarot_delay = 1.5
    cards = list(TAROT.glob('*.jpg'))
    captions = ['Прошлое', 'Настоящее', 'Будущее']
    user_random_cards = []
    tarot_messages = []

    sent_message = await message.answer(
        text='<b>Расклад Таро - это всего лишь инструмент для '
        'ознакомления и развлечения. '
        'Расклад карт Таро не является истиной и не должен '
        'использоваться для принятия важных решений.</b>'
        '\n'
        f'\n<u>{ORG_NAME}</u> и его сотрудники не несут '
        'ответственности за любые действия и их последствия, '
        'которые повлекло использование данного расклада карт Таро.'
    )
    await sleep(tarot_delay)

    while len(user_random_cards) < 3:
        card = choice(cards)
        card_num = int(card.stem)

        if card_num not in [int(c.stem) for c in user_random_cards]:
            if (card_num % 2 == 1 and card_num + 1 not in
                    [int(c.stem) for c in user_random_cards]):
                user_random_cards.append(card)
            elif (card_num % 2 == 0 and card_num - 1 not in
                  [int(c.stem) for c in user_random_cards]):
                user_random_cards.append(card)

    for card, caption in zip(user_random_cards, captions):
        photo = FSInputFile(card)
        text_file = card.with_suffix('.txt')
        with text_file.open(encoding='utf-8') as text:
            description = text.read()

        tarot_message = await BOT.send_photo(
            chat_id=message.chat.id,
            photo=photo,
            caption=f'<b>{caption}</b>: {description}'
        )

        tarot_messages.append(tarot_message)
        await sleep(tarot_delay)

    await record_message_id_to_db(sent_message, *tarot_messages)
