from asyncio import run
from logging import basicConfig, INFO

from aiogram import Dispatcher

from core.database.background_tasks import morning_routine
from core.handlers.admin_router import admin_router
from core.handlers.callback_router import callback_router
from core.handlers.directions_router import directions_router
from core.handlers.misc_router import misc_router
from core.handlers.shop_router import shop_router
from core.handlers.text_router import text_router
from core.handlers.user_router import user_router
from core.middleware.settings import BOT
from core.utils.broadcast import broadcast_router


async def bot_main():
    basicConfig(
        level=INFO,
        format='[%(levelname)s] %(asctime)s %(name)s: '
               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
    )

    dp = Dispatcher()

    dp.startup.register(morning_routine)
    dp.include_routers(
        admin_router,
        broadcast_router,
        user_router,
        callback_router,
        shop_router,
        directions_router,
        text_router,
        misc_router
    )

    try:
        await dp.start_polling(BOT)
    finally:
        await BOT.session.close()

if __name__ == '__main__':
    run(bot_main())
