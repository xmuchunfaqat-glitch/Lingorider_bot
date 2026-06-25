"""
Talaffuz va erkin gapirish mashqi oqimi:
1) Botning to'g'ri talaffuz namunasi (TTS audio) yuboriladi
2) Foydalanuvchi ovozli xabar yuboradi (talaffuz qilib yoki erkin gapirib)
3) Whisper orqali matnga aylantiriladi va maqsadli matn bilan solishtiriladi
4) Natija foiz va izoh bilan qaytariladi, adminga hisobot yuboriladi

Mashq paytida foydalanuvchi pauza qilishi (keyin xuddi shu jumladan davom
etish) yoki to'liq to'xtatishi mumkin.
"""
import json
import os
import random
import uuid

from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile
from pydub import AudioSegment

from config import LANGUAGES, VOICE_TMP_DIR
import database
import tts_service
import stt_service
import pronunciation_checker
import report_service
from states import ExerciseFlow
import texts
import keyboards

router = Router()

os.makedirs(VOICE_TMP_DIR, exist_ok=True)

_PHRASES_PATH = os.path.join(os.path.dirname(__file__), "phrases.json")
with open(_PHRASES_PATH, "r", encoding="utf-8") as f:
    PHRASES = json.load(f)


async def _send_phrase_prompt(message: Message, state: FSMContext, phrase: str, language_key: str):
    """Berilgan jumla uchun audio namuna va ovoz kutish klaviaturasini yuboradi."""
    audio_path = tts_service.generate_reference_audio(phrase, language_key)
    await message.answer_voice(FSInputFile(audio_path))
    await message.answer(
        texts.EXERCISE_PROMPT_TEXT.format(text=phrase),
        reply_markup=keyboards.exercise_wait_keyboard(),
    )
    await state.update_data(target_text=phrase, language_key=language_key, paused=False)
    await state.set_state(ExerciseFlow.waiting_voice)


async def _send_new_phrase(message: Message, state: FSMContext, language_key: str):
    phrase = random.choice(PHRASES[language_key])
    await message.answer(texts.EXERCISE_INTRO)
    await _send_phrase_prompt(message, state, phrase, language_key)


@router.message(F.text == "🎯 Talaffuz mashqi")
async def start_exercise(message: Message, state: FSMContext):
    user = await database.get_user(message.from_user.id)
    if not user or not user.onboarding_complete:
        await message.answer(texts.RESTART_PROFILE)
        return

    data = await state.get_data()
    if data.get("paused") and data.get("target_text"):
        # Pauza qilingan mashqni xuddi shu jumladan davom ettiramiz
        await message.answer(texts.EXERCISE_RESUMED)
        await _send_phrase_prompt(message, state, data["target_text"], data["language_key"])
        return

    await _send_new_phrase(message, state, user.target_language)


@router.message(ExerciseFlow.waiting_voice, F.voice)
async def process_voice_answer(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    target_text = data.get("target_text")
    language_key = data.get("language_key")

    await message.answer(texts.EXERCISE_ANALYZING)

    ogg_path = os.path.join(VOICE_TMP_DIR, f"{uuid.uuid4()}.ogg")
    wav_path = ogg_path.replace(".ogg", ".wav")
    try:
        file_info = await bot.get_file(message.voice.file_id)
        await bot.download_file(file_info.file_path, ogg_path)

        AudioSegment.from_file(ogg_path).export(wav_path, format="wav")

        whisper_lang = LANGUAGES[language_key]["whisper"]
        heard_text = stt_service.transcribe(wav_path, whisper_lang)
        result = pronunciation_checker.score_pronunciation(target_text, heard_text)
    finally:
        for p in (ogg_path, wav_path):
            if os.path.exists(p):
                os.remove(p)

    tier = pronunciation_checker.feedback_tier(result["score"])
    if tier == "great":
        text = texts.EXERCISE_RESULT_GREAT.format(score=result["score"], heard=result["heard"] or "—")
    elif tier == "ok":
        text = texts.EXERCISE_RESULT_OK.format(score=result["score"], target=target_text, heard=result["heard"] or "—")
    else:
        text = texts.EXERCISE_RESULT_BAD.format(score=result["score"], target=target_text, heard=result["heard"] or "—")

    await message.answer(text, reply_markup=keyboards.exercise_result_keyboard())

    await database.log_exercise(
        user_id=message.from_user.id,
        language=language_key,
        target_text=target_text,
        heard_text=result["heard"],
        score=result["score"],
        is_correct=result["is_correct"],
    )

    user = await database.get_user(message.from_user.id)
    await report_service.send_exercise_completed_report(
        bot,
        {"telegram_id": user.telegram_id, "full_name": user.full_name},
        {"language": LANGUAGES[language_key]["label"], "score": result["score"]},
    )


@router.message(ExerciseFlow.waiting_voice)
async def process_non_voice(message: Message):
    await message.answer(texts.EXERCISE_NO_VOICE)


@router.callback_query(F.data == "exercise:retry")
async def retry_exercise(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    target_text = data.get("target_text")
    language_key = data.get("language_key")
    await _send_phrase_prompt(callback.message, state, target_text, language_key)
    await callback.answer()


@router.callback_query(F.data == "exercise:next")
async def next_exercise(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    language_key = data.get("language_key")
    await callback.answer()
    await _send_new_phrase(callback.message, state, language_key)


@router.callback_query(F.data == "exercise:pause")
async def pause_exercise(callback: CallbackQuery, state: FSMContext):
    # State'ni emas, faqat aktiv kutishni to'xtatamiz - target_text/language_key
    # ma'lumotlari saqlanib qoladi, keyinroq xuddi shu jumladan davom etamiz.
    await state.update_data(paused=True)
    await state.set_state(None)
    await callback.message.answer(texts.EXERCISE_PAUSED, reply_markup=keyboards.main_menu_keyboard())
    await callback.answer()


@router.callback_query(F.data == "exercise:stop")
async def stop_exercise(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(texts.EXERCISE_FINISHED, reply_markup=keyboards.main_menu_keyboard())
    await callback.answer()
