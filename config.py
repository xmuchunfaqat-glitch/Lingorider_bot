"""
Lingorider_bot — markaziy sozlamalar fayli.
Barcha muhit o'zgaruvchilari (.env) shu yerdan o'qiladi.
"""
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "small")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Tashkent")

# Bot o'rgatadigan tillar va ularning gTTS / Whisper kodlari
LANGUAGES = {
    "ingliz": {"label": "🇬🇧 Ingliz tili", "gtts": "en", "whisper": "en"},
    "rus": {"label": "🇷🇺 Rus tili", "gtts": "ru", "whisper": "ru"},
    "ispan": {"label": "🇪🇸 Ispan tili", "gtts": "es", "whisper": "es"},
    "turk": {"label": "🇹🇷 Turk tili", "gtts": "tr", "whisper": "tr"},
    "nemis": {"label": "🇩🇪 Nemis tili", "gtts": "de", "whisper": "de"},
    "xitoy": {"label": "🇨🇳 Xitoy tili", "gtts": "zh-CN", "whisper": "zh"},
    "italyan": {"label": "🇮🇹 Italyan tili", "gtts": "it", "whisper": "it"},
}

# O'zbekiston viloyatlari
REGIONS = [
    "Toshkent shahri", "Toshkent viloyati", "Andijon", "Buxoro",
    "Farg'ona", "Jizzax", "Xorazm", "Namangan", "Navoiy",
    "Qashqadaryo", "Qoraqalpog'iston Respublikasi", "Samarqand",
    "Sirdaryo", "Surxondaryo",
]

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "lingorider.db")
AUDIO_CACHE_DIR = os.path.join(os.path.dirname(__file__), "data", "audio_cache")
VOICE_TMP_DIR = os.path.join(os.path.dirname(__file__), "data", "voice_tmp")

REPORT_INTERVAL_MINUTES = 30
