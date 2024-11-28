from asyncio import run

from aiogram import Dispatcher
from aiogram.types import BotCommand

from core.database.background_tasks import morning_routine
from core.routers.maintenance_router import maintenance_router
from core.routers.main_router import main_router
from core.middleware.settings import BOT, MAINTENANCE_MODE, COMMANDS
from core.utils.broadcast import broadcast_router
from core.utils.proportions import proportions_router


async def bot_main():
    """
    Main bot logic function. Contains: Dispatcher object, all the routers and
    infinity polling instruction.

    :return: None
    """

    dp = Dispatcher()

    if MAINTENANCE_MODE:
        await BOT.set_my_commands(
            [BotCommand(command='start', description='Запуск бота')]
        )

        dp.include_router(maintenance_router)
    else:
        await BOT.set_my_commands(COMMANDS)

        dp.startup.register(morning_routine)

        dp.include_routers(
            broadcast_router,
            proportions_router,
            main_router
        )

    await dp.start_polling(BOT)


if __name__ == '__main__':
    run(bot_main())
