"""
AI maslahat xizmati — Google Gemini (bepul tarif, https://aistudio.google.com/apikey).
Gemini SDK sinxron ishlaydi, shu sababli asyncio.to_thread bilan chaqiramiz,
toki bot bloklanib qolmasin.
"""
import asyncio

import google.generativeai as genai

from config import GEMINI_API_KEY

_SYSTEM_PROMPT = (
    "Sen Lingorider botining til o'rgatuvchi sun'iy intellekt yordamchisisan. "
    "Foydalanuvchilar — o'zbek yoshlari va til o'rganishga qiziqqan insonlar. "
    "Javoblaringni FAQAT o'zbek tilida, qisqa (3-5 jumla), iliq, ilhomlantiruvchi va "
    "amaliy maslahatlar bilan yoz. Murakkab atamalardan qoch, oddiy tilda gapir."
)

_configured = False


def _ensure_configured():
    global _configured
    if not _configured and GEMINI_API_KEY:
        genai.configure(api_key=GEMINI_API_KEY)
        _configured = True


def _generate_sync(prompt: str) -> str:
    _ensure_configured()
    model = genai.GenerativeModel(
        # Eslatma: Google modellarni vaqti-vaqti bilan yangilaydi/eskirtiradi.
        # Joriy bepul tarifdagi modellar ro'yxati: https://ai.google.dev/gemini-api/docs/models
        # "gemini-2.5-flash" — yozilgan vaqtda barqaror (stable) va bepul tarifda mavjud.
        model_name="gemini-2.5-flash",
        system_instruction=_SYSTEM_PROMPT,
    )
    response = model.generate_content(prompt)
    return response.text.strip()


async def get_personal_advice(profile: dict) -> str:
    prompt = (
        f"Foydalanuvchi profili:\n"
        f"- Ism: {profile.get('full_name')}\n"
        f"- Yosh: {profile.get('age')}\n"
        f"- Maqsad: {profile.get('goal')}\n"
        f"- O'rganayotgan til: {profile.get('target_language')}\n"
        f"- Kunlik mashg'uloti: {profile.get('daily_routine')}\n"
        f"- E'tibor qaratmoqchi bo'lgan soha: {profile.get('focus_area')}\n\n"
        "Shu profilga mos, bugun u amalga oshirishi mumkin bo'lgan aniq va qisqa "
        "til o'rganish maslahati ber."
    )
    return await asyncio.to_thread(_generate_sync, prompt)


async def get_language_recommendation(goal: str) -> str:
    prompt = (
        f"Foydalanuvchining tilni o'rganish maqsadi: \"{goal}\". "
        "Ingliz, rus, ispan, turk, nemis, xitoy, italyan tillaridan qaysi biri "
        "unga eng mos kelishini tanlab, sababini qisqa tushuntir."
    )
    return await asyncio.to_thread(_generate_sync, prompt)
