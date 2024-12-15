from asyncio import run

from aiogram import Dispatcher
from aiogram.types import BotCommand

from core.database.background_tasks import morning_routine
from core.database.middleware import CheckUserDataBaseMiddleware
from core.components.settings import BOT, MAINTENANCE_MODE, COMMANDS
from core.routers.admin_router import admin_router
from core.routers.directions_router import directions_router
from core.routers.main_router import main_router
from core.routers.maintenance_router import maintenance_router
from core.routers.shop_router import shop_router
from core.routers.utils_router import utils_router


async def bot_main():
    """
    Main bot logic function. Contains: Dispatcher object, all the routers and
    infinity polling instruction.

    :return: None
    """

    dp = Dispatcher()
    dp.message.outer_middleware(CheckUserDataBaseMiddleware())

    if MAINTENANCE_MODE:
        await BOT.set_my_commands(
            [BotCommand(command='start', description='Запуск бота')]
        )

        dp.include_router(maintenance_router)
    else:
        await BOT.set_my_commands(COMMANDS)

        dp.startup.register(morning_routine)

        dp.include_routers(
            utils_router,
            admin_router,
            directions_router,
            shop_router,
            main_router
        )

    await dp.start_polling(BOT)


if __name__ == '__main__':
    run(bot_main())
