from asyncio import sleep
from pathlib import Path
from random import choice

from aiogram.types import Message, FSInputFile

from core.database.background_tasks import record_message_id_to_db
from core.middleware.settings import BOT, ORG_NAME


async def tarot_main(message: Message):
    """
    Handle the main logic for a tarot card reading. This function sends an
    introductory disclaimer message, selects 3 random tarot cards, and sends
    their images with descriptions to the user.

    :param message: The message sent by the user.
    :return:
    """

    tarot_delay = 1.5
    tarot_path = Path(__file__).parent.parent.parent / '..' / 'Tarot'
    cards = list(tarot_path.glob('*.jpg'))
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
