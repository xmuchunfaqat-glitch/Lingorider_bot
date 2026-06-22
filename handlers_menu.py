"""
Asosiy menyu tugmalari: AI maslahat, natijalar va sozlamalar.
"""
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from config import LANGUAGES
import database
import gemini_service
from states import SettingsFlow
import texts
import keyboards

router = Router()


@router.message(F.text == "🤖 AI maslahat")
async def ai_advice(message: Message):
    user = await database.get_user(message.from_user.id)
    if not user or not user.onboarding_complete:
        await message.answer(texts.RESTART_PROFILE)
        return

    thinking_msg = await message.answer(texts.AI_ADVICE_THINKING)
    try:
        advice = await gemini_service.get_personal_advice({
            "full_name": user.full_name,
            "age": user.age,
            "goal": user.goal,
            "target_language": LANGUAGES[user.target_language]["label"],
            "daily_routine": user.daily_routine,
            "focus_area": user.focus_area,
        })
    except Exception:
        advice = texts.AI_ADVICE_ERROR
    await thinking_msg.edit_text(advice)


@router.message(F.text == "📊 Mening natijalarim")
async def my_stats(message: Message):
    user = await database.get_user(message.from_user.id)
    if not user or not user.onboarding_complete:
        await message.answer(texts.RESTART_PROFILE)
        return
    stats = await database.get_user_stats(message.from_user.id)
    await message.answer(
        texts.PROFILE_STATS_TEMPLATE.format(
            language=LANGUAGES[user.target_language]["label"],
            total=stats["total"],
            avg_score=stats["avg_score"],
            last_date=stats["last_date"],
        )
    )


@router.message(F.text == "⚙️ Sozlamalar")
async def settings_menu(message: Message):
    await message.answer("Sozlamalar:", reply_markup=keyboards.settings_menu_keyboard())


@router.message(F.text == "⬅️ Orqaga")
async def back_to_main(message: Message):
    await message.answer("Bosh menyu:", reply_markup=keyboards.main_menu_keyboard())


@router.message(F.text == "🌐 Tilni o'zgartirish")
async def change_language(message: Message, state: FSMContext):
    await message.answer(texts.ASK_LANGUAGE, reply_markup=keyboards.language_keyboard())
    await state.set_state(SettingsFlow.waiting_language)


@router.callback_query(SettingsFlow.waiting_language, F.data.startswith("lang:"))
async def process_language_change(callback: CallbackQuery, state: FSMContext):
    lang_key = callback.data.split(":", 1)[1]
    if lang_key == "unsure":
        await callback.answer("Iltimos, ro'yxatdan birini tanlang", show_alert=True)
        return
    await database.update_user(callback.from_user.id, target_language=lang_key)
    await state.clear()
    await callback.message.edit_text(texts.LANGUAGE_CHANGED.format(language=LANGUAGES[lang_key]["label"]))
    await callback.message.answer("Bosh menyu:", reply_markup=keyboards.main_menu_keyboard())
    await callback.answer()


@router.message(F.text == "🔁 Profilni qayta to'ldirish")
async def restart_profile(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts.RESTART_PROFILE)
