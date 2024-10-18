from asyncio import sleep

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.background_tasks import (
    record_message_id_to_db,
    get_users_count
)
from core.keyboards.admin_kb import admin_keyboard
from core.keyboards.proportiom_kb import proportion_keyboard
from core.middleware.fsm import ProportionStates
from core.middleware.settings import DEL_TIME, BOT
from core.middleware.wrappers import check_is_admin
from core.utils.broadcast import start_broadcast

admin_router = Router()


@admin_router.callback_query(F.data == 'admin')
async def callback_admin(callback: CallbackQuery):
    """
    Handles the 'help' callback query. Responds to the user and
    triggers the help command.

    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    message = callback.message

    await message.delete()
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text='<b>Добро пожаловать в админское меню!</b>'
             '\n'
             '\n/broadcast - Начать процедуру рассылки'
             '\n'
             '\n/users - Узнать сколько пользователей в БД'
             '\n'
             '\n/proportions - Калькулятор пропорций',
        reply_markup=admin_keyboard
    )

    await record_message_id_to_db(sent_message)


@admin_router.message(Command('users'))
@check_is_admin
async def send_user_count(message: Message):
    """
    Handles the 'users' command. Responds to the admin-user and sends the
    user count.

    :param message: The message sent by the user.
    :return: None
    """

    count = await get_users_count()

    await message.delete()
    await sleep(DEL_TIME)

    sent_message = await message.answer(
        text=f'Количество пользователей в БД: {count}'
    )

    await sleep(3.5)
    await BOT.delete_message(message.chat.id, sent_message.message_id)


@admin_router.message(Command('broadcast'))
@check_is_admin
async def cmd_broadcast(message: Message, state: FSMContext):
    """
    Handles the 'broadcast' command. Responds to the admin-user and starts a
    broadcast sequence.

    :param state: FSM context containing the state data.
    :param message: The message sent by the user.
    :return: None
    """

    await start_broadcast(message, state=state)


@admin_router.message(Command('proportions'))
@check_is_admin
async def proportions(
        message: Message,
        state: FSMContext,
        keep_last_msg: bool = False
):

    """
    Handles the 'proportions' command. Receive a str value from admin and
    triggers the calculate_proportion function.

    :param state: FSM context containing the state data.
    :param keep_last_msg: A boolean value that determines whether the previous
                          message will be deleted.
    :param message: The message sent by the user.
    :return: None
    """

    if not keep_last_msg:
        await message.delete()
        await sleep(DEL_TIME)

    await state.set_state(ProportionStates.waiting_for_proportion_input)
    sent_message = await message.answer(
        text='Введите через пробел: '
             '\nПропорции компонентов '
             '<b>A</b> и <b>B</b>, '
             'и общую массу - <b>C</b>'
    )

    await record_message_id_to_db(sent_message)


@admin_router.callback_query(F.data == 'another_proportion')
async def callback_proportion(callback: CallbackQuery, state: FSMContext):

    """
    Handles the 'another_proportion' callback query. Responds to the admin and
    triggers the proportions command.

    :param state: FSM context containing the state data.
    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()
    await proportions(callback.message, state=state, keep_last_msg=True)


@admin_router.message(ProportionStates.waiting_for_proportion_input)
async def calculate_proportion(message: Message, state: FSMContext):
    """
    Processes user input for component proportions, validates the input,
    performs calculations, and sends the result back to the user.

    :param state: FSM context for managing the user's state.
    :param message: The message sent by the user.
    :return: None
    """

    await record_message_id_to_db(message)

    def is_number(item):
        try:
            float(item)
            return True
        except ValueError:
            return False

    prop_input_split = message.text.replace(',', '.').split()
    digit_check = all(is_number(item) for item in prop_input_split)

    if len(prop_input_split) == 3 and digit_check:
        a_input, b_input, c_input = map(float, prop_input_split)

        a_gr = (c_input / (a_input + b_input)) * a_input
        b_gr = (c_input / (a_input + b_input)) * b_input

        a_percent = 100 / (a_gr + b_gr) * a_gr
        b_percent = 100 / (a_gr + b_gr) * b_gr

        a_part_new = int(a_percent) if a_percent.is_integer() \
            else round(a_percent, 2)
        b_part_new = int(b_percent) if b_percent.is_integer() \
            else round(b_percent, 2)

        a_new = int(a_gr) if a_gr.is_integer() else round(a_gr, 2)
        b_new = int(b_gr) if b_gr.is_integer() else round(b_gr, 2)
        c_new = int(c_input) if c_input.is_integer() else round(c_input, 2)

        reply_text = (
            f'Для раствора массой: <b>{c_new} гр.</b>\nНеобходимо:'
            f'\n<b>{a_new} гр.</b> Компонента <b>A</b> ({a_part_new} %)'
            f'\n<b>{b_new} гр.</b> Компонента <b>B</b> ({b_part_new} %)'
        )

        sent_message = await message.reply(
            reply_text,
            reply_markup=proportion_keyboard
        )
    else:
        reply_text = (
            'Неверный формат данных.'
            '\nПожалуйста, введите числа по образцу:\n<b>A B C</b>'
        )
        sent_message = await message.reply(
            reply_text
        )

    await record_message_id_to_db(sent_message)

    await state.clear()
