"""
/start bilan boshlanadigan tanishuv (onboarding) oqimi.
Ism, yosh, hudud, maqsad, til, kunlik tartib va e'tibor sohasini so'raydi,
ma'lumotlar bazasiga yozadi va adminga hisobot yuboradi.
"""
from aiogram import Router, F, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import LANGUAGES
import database
import report_service
import gemini_service
from states import Onboarding
import texts
import keyboards

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await database.get_or_create_user(message.from_user.id)
    await message.answer(texts.WELCOME)
    await message.answer(texts.ASK_NAME)
    await state.set_state(Onboarding.waiting_name)


@router.message(Onboarding.waiting_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text.strip())
    await message.answer(texts.ASK_AGE)
    await state.set_state(Onboarding.waiting_age)


@router.message(Onboarding.waiting_age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.strip().isdigit():
        await message.answer(texts.ASK_AGE_INVALID)
        return
    await state.update_data(age=int(message.text.strip()))
    await message.answer(texts.ASK_REGION, reply_markup=keyboards.regions_keyboard())
    await state.set_state(Onboarding.waiting_region)


@router.callback_query(Onboarding.waiting_region, F.data.startswith("region:"))
async def process_region(callback: CallbackQuery, state: FSMContext):
    region = callback.data.split(":", 1)[1]
    await state.update_data(region=region)
    await callback.message.edit_text(f"📍 Viloyat: <b>{region}</b>")
    await callback.message.answer(texts.ASK_DISTRICT)
    await state.set_state(Onboarding.waiting_district)
    await callback.answer()


@router.message(Onboarding.waiting_district)
async def process_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text.strip())
    await message.answer(texts.ASK_GOAL, reply_markup=keyboards.goal_keyboard())
    await state.set_state(Onboarding.waiting_goal)


@router.callback_query(Onboarding.waiting_goal, F.data.startswith("goal:"))
async def process_goal(callback: CallbackQuery, state: FSMContext):
    goal = callback.data.split(":", 1)[1]
    await state.update_data(goal=goal)
    await callback.message.edit_text(f"🎯 Maqsad: <b>{goal}</b>")
    await callback.message.answer(texts.ASK_LANGUAGE, reply_markup=keyboards.language_keyboard())
    await state.set_state(Onboarding.waiting_language)
    await callback.answer()


@router.callback_query(Onboarding.waiting_language, F.data.startswith("lang:"))
async def process_language(callback: CallbackQuery, state: FSMContext):
    lang_key = callback.data.split(":", 1)[1]
    data = await state.get_data()

    if lang_key == "unsure":
        await callback.message.edit_text(texts.AI_ADVICE_THINKING)
        try:
            recommendation = await gemini_service.get_language_recommendation(data.get("goal", ""))
        except Exception:
            recommendation = (
                "Maqsadingiz uchun eng mashhur tanlov — Ingliz tili, chunki u ish, "
                "sayohat va o'qish uchun eng ko'p qo'llaniladi."
            )
        await callback.message.answer(recommendation)
        await callback.message.answer(texts.ASK_LANGUAGE, reply_markup=keyboards.language_keyboard())
        await callback.answer()
        return

    label = LANGUAGES[lang_key]["label"]
    await state.update_data(target_language=lang_key)
    await callback.message.edit_text(f"🗣 Til: <b>{label}</b>")
    await callback.message.answer(texts.ASK_DAILY_ROUTINE)
    await state.set_state(Onboarding.waiting_daily_routine)
    await callback.answer()


@router.message(Onboarding.waiting_daily_routine)
async def process_daily_routine(message: Message, state: FSMContext):
    await state.update_data(daily_routine=message.text.strip())
    await message.answer(texts.ASK_FOCUS_AREA, reply_markup=keyboards.focus_keyboard())
    await state.set_state(Onboarding.waiting_focus_area)


@router.callback_query(Onboarding.waiting_focus_area, F.data.startswith("focus:"))
async def process_focus_area(callback: CallbackQuery, state: FSMContext, bot: Bot):
    focus = callback.data.split(":", 1)[1]
    await state.update_data(focus_area=focus)
    data = await state.get_data()

    user = await database.update_user(
        callback.from_user.id,
        full_name=data.get("full_name"),
        age=data.get("age"),
        region=data.get("region"),
        district=data.get("district"),
        goal=data.get("goal"),
        target_language=data.get("target_language"),
        daily_routine=data.get("daily_routine"),
        focus_area=focus,
        onboarding_complete=True,
    )

    language_label = LANGUAGES[data["target_language"]]["label"]
    await callback.message.edit_text(f"🔎 E'tibor sohasi: <b>{focus}</b>")
    await callback.message.answer(
        texts.ONBOARDING_DONE.format(name=user.full_name, language=language_label),
        reply_markup=keyboards.main_menu_keyboard(),
    )
    await callback.answer()
    await state.clear()

    # Adminga DARROV hisobot yuborish (yangi foydalanuvchi)
    await report_service.send_new_user_report(bot, {
        "telegram_id": user.telegram_id,
        "full_name": user.full_name,
        "age": user.age,
        "region": user.region,
        "district": user.district,
        "goal": user.goal,
        "target_language": language_label,
        "daily_routine": user.daily_routine,
        "focus_area": user.focus_area,
    })
