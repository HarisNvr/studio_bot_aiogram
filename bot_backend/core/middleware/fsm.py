from aiogram.fsm.state import State, StatesGroup


class ProportionStates(StatesGroup):
    waiting_for_proportion_input = State()
