import logging
from asyncio import run

from aiogram import Dispatcher

from bot_backend.core.database.background_tasks import morning_routine
from core.middleware.settings import BOT


async def bot_main():
    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(asctime)s %(name)s: '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    )

    dp = Dispatcher()

    dp.startup.register(morning_routine)

    try:
        await dp.start_polling(BOT)
    finally:
        await BOT.session.close()

if __name__ == '__main__':
    run(bot_main())
