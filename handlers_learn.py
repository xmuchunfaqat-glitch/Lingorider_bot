"""
Grammatika va Lug'at boyligi — yozma (matn) ko'rinishidagi o'quv bo'limlari.
Ovozli xabar talab qilinmaydi, faqat o'qish uchun.
"""
import json
import os

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from config import LANGUAGES
import database
import texts
import keyboards

router = Router()

_GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), "grammar.json")
_VOCAB_PATH = os.path.join(os.path.dirname(__file__), "vocabulary.json")

with open(_GRAMMAR_PATH, "r", encoding="utf-8") as f:
    GRAMMAR = json.load(f)

with open(_VOCAB_PATH, "r", encoding="utf-8") as f:
    VOCABULARY = json.load(f)


async def _require_profile(message: Message):
    user = await database.get_user(message.from_user.id)
    if not user or not user.onboarding_complete:
        await message.answer(texts.RESTART_PROFILE)
        return None
    return user


@router.message(F.text == "📚 Grammatika")
async def grammar_menu(message: Message):
    user = await _require_profile(message)
    if not user:
        return
    topics = GRAMMAR.get(user.target_language, [])
    label = LANGUAGES[user.target_language]["label"]
    await message.answer(
        texts.GRAMMAR_CHOOSE_TOPIC.format(language=label),
        reply_markup=keyboards.grammar_topics_keyboard(topics),
    )


@router.callback_query(F.data.startswith("grammar:"))
async def grammar_topic(callback: CallbackQuery):
    user = await database.get_user(callback.from_user.id)
    if not user:
        await callback.answer()
        return
    topics = GRAMMAR.get(user.target_language, [])
    index = int(callback.data.split(":", 1)[1])
    if 0 <= index < len(topics):
        topic = topics[index]
        await callback.message.answer(f"📚 <b>{topic['title']}</b>\n\n{topic['body']}")
    await callback.answer()


@router.message(F.text == "🧠 Lug'at boyligi")
async def vocab_menu(message: Message):
    user = await _require_profile(message)
    if not user:
        return
    categories = list(VOCABULARY.get(user.target_language, {}).keys())
    label = LANGUAGES[user.target_language]["label"]
    await message.answer(
        texts.VOCAB_CHOOSE_CATEGORY.format(language=label),
        reply_markup=keyboards.vocab_categories_keyboard(categories),
    )


@router.callback_query(F.data.startswith("vocab:"))
async def vocab_category(callback: CallbackQuery):
    user = await database.get_user(callback.from_user.id)
    if not user:
        await callback.answer()
        return
    category = callback.data.split(":", 1)[1]
    words = VOCABULARY.get(user.target_language, {}).get(category, [])
    lines = [
        texts.VOCAB_WORD_LINE.format(
            word=w["word"], pronunciation=w["pronunciation"], meaning=w["meaning"]
        )
        for w in words
    ]
    await callback.message.answer(f"🧠 <b>{category}</b>\n\n" + "\n".join(lines))
    await callback.answer()
