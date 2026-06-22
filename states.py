from aiogram.fsm.state import StatesGroup, State


class Onboarding(StatesGroup):
    waiting_name = State()
    waiting_age = State()
    waiting_region = State()
    waiting_district = State()
    waiting_goal = State()
    waiting_language = State()
    waiting_daily_routine = State()
    waiting_focus_area = State()


class ExerciseFlow(StatesGroup):
    waiting_voice = State()


class SettingsFlow(StatesGroup):
    waiting_language = State()
