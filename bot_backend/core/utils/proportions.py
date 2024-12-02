from asyncio import sleep
from decimal import Decimal, ROUND_HALF_UP

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from core.database.background_tasks import record_message_id_to_db
from core.keyboards.utils_kbs import (
    cancel_proportion_keyboard, another_proportion_keyboard
)
from core.middleware.fsm import ProportionStates
from core.middleware.settings import DEL_TIME, BOT
from core.middleware.wrappers import check_bd_chat_id

proportions_router = Router()


def calculate_proportion(user_input: list[str]) -> str | None:
    """
    Calculate the proportion of components A and B in a mixture C, based
    on user input.

    The function validates the input, computes the proportions of components
    A and B as percentages, and calculates the required mass of each component
    to form a mixture with the given total mass. Results are rounded to two
    decimal places and formatted into kilograms and grams.

    :param user_input: A list of strings possibly representing the masses of
                       components A, B, and the total mixture mass
                       respectively. All values must be positive.
    :return: A formatted string detailing the proportions and masses of
             components A and B, along with the total mixture mass, or None.
    """

    condition_one = len(user_input) == 3
    condition_two = False
    condition_three = False
    result = []

    if condition_one:
        condition_two = all(
            num.replace(
                '.', '', 1
            ).isdigit() for num in user_input
        )

    if condition_two:
        condition_three = all(float(num) > 0 for num in user_input)

    if condition_three:
        a_input, b_input, c_input = map(Decimal, user_input)

        a_percent = Decimal(100) / (a_input + b_input) * a_input
        a_percent = a_percent.quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        b_percent = Decimal(100) - a_percent
        b_percent = b_percent.quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        component_a = c_input / (a_input + b_input) * a_input
        component_a = component_a.quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        component_b = c_input - component_a
        component_b = component_b.quantize(
            Decimal('0.01'),
            rounding=ROUND_HALF_UP
        )

        for component in (component_a, component_b, c_input):
            kilograms = component // Decimal(1000)
            grams = component % Decimal(1000)

            if kilograms:
                result.append(f'{kilograms} кг. {grams} гр.')
            else:
                result.append(f'{grams} гр.')

        reply_text = (
            f'Для раствора массой: <b>{result[2]}</b>\nНеобходимо:'
            f'\n<b>{result[0]}</b> Компонента <b>A</b> ({a_percent} %)'
            f'\n<b>{result[1]}</b> Компонента <b>B</b> ({b_percent} %)'
        )

        return reply_text


@check_bd_chat_id
@proportions_router.message(Command('proportions'))
async def proportions(
        message: Message,
        state: FSMContext,
        keep_last_msg: bool = False
):
    """
    Handles the 'proportions' command. Receive a str value from user and
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

        proportions_text = (
            'Введите через пробел пропорции компонентов в долях и общую массу.'
            '\nНапример:'
            '\n\n4 части или 40% компонента - <b>(A)</b>'
            '\n6 частей или 60% компонента - <b>(B)</b>'
            '\nОбщая масса 1500 грамм - <b>(C)</b>'
            '\n\nПример ввода: <b>4 6 1500</b>'
        )
    else:
        proportions_text = (
            'Введите через пробел пропорции компонентов в долях и общую массу.'
            '\n\nПример ввода: <b>4 6 1500</b>'
        )

    await state.set_state(ProportionStates.waiting_for_proportion_input)
    sent_message = await message.answer(
        text=proportions_text,
        reply_markup=cancel_proportion_keyboard
    )

    await record_message_id_to_db(sent_message)


@proportions_router.callback_query(F.data == 'cancel_proportion')
async def cancel_proportion(callback: CallbackQuery, state: FSMContext):
    """
    Handles the 'cancel_proportion' callback query. Responds to the user and
    cancels the proportions command.

    :param state: FSM context containing the state data.
    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()

    await state.clear()

    await callback.message.delete()


@proportions_router.callback_query(F.data == 'another_proportion')
async def callback_proportion(callback: CallbackQuery, state: FSMContext):
    """
    Handles the 'another_proportion' callback query. Responds to the user and
    triggers the proportions command.

    :param state: FSM context containing the state data.
    :param callback: The callback query object containing information about
                     the message and chat.
    :return: None
    """

    await callback.answer()

    await BOT.edit_message_reply_markup(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    await sleep(DEL_TIME)

    await proportions(callback.message, state=state, keep_last_msg=True)


@proportions_router.message(ProportionStates.waiting_for_proportion_input)
async def send_proportion(message: Message, state: FSMContext):
    """
    Processes user input for component proportions, validates the input,
    performs calculations, and sends the result back to the user.

    :param state: FSM context for managing the user's state.
    :param message: The message sent by the user.
    :return: None
    """

    chat_id = message.chat.id
    message_id = message.message_id
    previous_message_id = message_id - 1

    await BOT.delete_messages(
        chat_id=chat_id,
        message_ids=[message_id, previous_message_id]
    )
    await sleep(DEL_TIME)

    input_split = message.text.replace(',', '.').split()
    result = calculate_proportion(input_split)

    if result:
        sent_message = await message.answer(
            text=result,
            reply_markup=another_proportion_keyboard
        )
        await state.clear()
    else:
        sent_message = await message.answer(
            text='Неверный формат данных.'
                 '\nПожалуйста, введите положительные числа по образцу:'
                 '\n<b>A B C</b>',
            reply_markup=cancel_proportion_keyboard
        )

    await record_message_id_to_db(message, sent_message)
