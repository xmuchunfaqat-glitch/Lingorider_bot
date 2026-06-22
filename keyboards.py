"""
Qayta ishlatiladigan klaviaturalar (reply va inline tugmalar).
"""
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from config import REGIONS, LANGUAGES
import texts


def regions_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for region in REGIONS:
        builder.button(text=region, callback_data=f"region:{region}")
    builder.adjust(2)
    return builder.as_markup()


def goal_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for goal in texts.GOAL_OPTIONS:
        builder.button(text=goal, callback_data=f"goal:{goal}")
    builder.adjust(1)
    return builder.as_markup()


def language_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for key, info in LANGUAGES.items():
        builder.button(text=info["label"], callback_data=f"lang:{key}")
    builder.button(text=texts.ASK_LANGUAGE_UNSURE, callback_data="lang:unsure")
    builder.adjust(2)
    return builder.as_markup()


def focus_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for focus in texts.FOCUS_OPTIONS:
        builder.button(text=focus, callback_data=f"focus:{focus}")
    builder.adjust(1)
    return builder.as_markup()


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for label in texts.MAIN_MENU_BUTTONS:
        builder.button(text=label)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def settings_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    for label in texts.SETTINGS_MENU_BUTTONS:
        builder.button(text=label)
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def exercise_result_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text=texts.EXERCISE_RETRY_BUTTON, callback_data="exercise:retry")
    builder.button(text=texts.EXERCISE_NEXT_BUTTON, callback_data="exercise:next")
    builder.button(text=texts.EXERCISE_STOP_BUTTON, callback_data="exercise:stop")
    builder.adjust(2, 1)
    return builder.as_markup()
