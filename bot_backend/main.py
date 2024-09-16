from asyncio import run
from logging import basicConfig, INFO

from aiogram import Dispatcher

from core.database.background_tasks import morning_routine
from core.handlers.admin_router import admin_router
from core.handlers.user_router import user_router
from core.middleware.settings import BOT


async def bot_main():
    basicConfig(
        level=INFO,
        format='[%(levelname)s] %(asctime)s %(name)s: '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    )

    dp = Dispatcher()

    dp.startup.register(morning_routine)
    dp.include_routers(admin_router, user_router)

    try:
        await dp.start_polling(BOT)
    finally:
        await BOT.session.close()

if __name__ == '__main__':
    run(bot_main())
