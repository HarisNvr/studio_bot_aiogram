from aiogram.fsm.state import State, StatesGroup


class ProportionStates(StatesGroup):
    """
    Defines the states for managing proportions in an FSM context.

    waiting_for_proportion_input: The state where the bot is waiting for the
    admin to input a proportion.
    """

    waiting_for_proportion_input = State()


class BroadcastStates(StatesGroup):
    """
    Defines the states for managing broadcasts in an FSM context.

    broadcast_message: The state where the bot is waiting for the message
    to be broadcast.
    """

    broadcast_message = State()

