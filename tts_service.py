"""
Bepul TTS xizmati — gTTS (Google Translate ovoz sintezi) orqali to'g'ri
talaffuz namunasini audio fayl sifatida tayyorlaydi. API kalit talab qilmaydi.
"""
import hashlib
import os

from gtts import gTTS

from config import AUDIO_CACHE_DIR, LANGUAGES

os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)


def _cache_path(text: str, lang_code: str) -> str:
    key = hashlib.md5(f"{lang_code}:{text}".encode("utf-8")).hexdigest()
    return os.path.join(AUDIO_CACHE_DIR, f"{key}.mp3")


def generate_reference_audio(text: str, language_key: str) -> str:
    """
    Berilgan matn uchun to'g'ri talaffuz audiosini qaytaradi (fayl yo'li).
    Bir xil matn/til uchun keshdan foydalanadi — qayta generatsiya qilmaydi.
    """
    lang_code = LANGUAGES[language_key]["gtts"]
    path = _cache_path(text, lang_code)
    if not os.path.exists(path):
        tts = gTTS(text=text, lang=lang_code, slow=False)
        tts.save(path)
    return path
